import os
import numpy as np
import pandas as pd
from nexcsi import decoder
from scipy.signal import butter, lfilter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GRU, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, confusion_matrix

# --- 1. 데이터 전처리: .pcap → CSI 진폭 데이터 생성 ---
def low_pass_filter(data, cutoff=0.1, fs=1.0, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return lfilter(b, a, data, axis=0)

def process_pcap_to_csv(pcap_folder, output_folder, device="raspberrypi"):
    os.makedirs(output_folder, exist_ok=True)  # 출력 폴더 생성
    null_subcarriers = [1, 2, 3, 4, 5, 6, 11, 25, 32, 39, 53, 60, 61, 62, 63]

    for file_name in os.listdir(pcap_folder):
        if not file_name.endswith(".pcap"):
            continue
        try:
            print(f"Processing {file_name}...")
            pcap_path = os.path.join(pcap_folder, file_name)
            output_path = os.path.join(output_folder, file_name.replace(".pcap", ".csv"))

            # .pcap 파일에서 CSI 데이터 추출
            samples = decoder(device).read_pcap(pcap_path)
            csi = decoder(device).unpack(samples['csi'], zero_nulls=False, zero_pilots=False)

            # 복소수 → 진폭 → 데시벨 변환
            amplitude = np.abs(csi)
            amplitude[amplitude == 0] = 1e-10  # 로그 오류 방지
            amplitude_db = 20 * np.log10(amplitude)

            # Null 및 파일럿 부반송파 제거
            csi_amplitude_cleaned = np.delete(amplitude_db, [i for i in null_subcarriers if i < amplitude_db.shape[1]], axis=1)

            # 저주파 통과 필터 적용
            filtered_data = low_pass_filter(csi_amplitude_cleaned)

            if filtered_data.size == 0:
                print(f"Warning: {file_name} 처리 결과가 비어 있습니다.")
                continue

            pd.DataFrame(filtered_data).to_csv(output_path, index=False)
            print(f"Saved to {output_path}")
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
            continue

# --- 2. 데이터 결합 ---
def combine_csv(input_folder, output_file):
    all_data = []
    for file_name in os.listdir(input_folder):
        if not file_name.endswith(".csv") or file_name == "combined_data.csv":  # combined_data.csv 제외
            continue
        try:
            df = pd.read_csv(os.path.join(input_folder, file_name))
            label = ''.join([c for c in file_name if not c.isdigit()]).replace(".csv", "")
            if label == 'loswal': label = 'loswalk'
            if label == 'losN#': label = 'losN'
            df['Label'] = label
            all_data.append(df)
        except Exception as e:
            print(f"Error reading {file_name}: {e}")

    if not all_data:
        print("No valid CSV files to combine. Exiting...")
        return

    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df.fillna(combined_df.select_dtypes(include=["number"]).median(), inplace=True)
    combined_df.to_csv(output_file, index=False)
    print(f"Combined CSV saved to {output_file}")

# --- 3. LoS/NLoS 식별 모델 학습 ---
def train_los_nlos_model(data_file):
    data = pd.read_csv(data_file)
    X = data.drop(columns=["Label"]).values
    y = LabelEncoder().fit_transform(data["Label"].apply(lambda x: "NLoS" if x.startswith("Nlos") else "LoS"))
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # 학습률 조정 (Adam 옵티마이저 사용)
    learning_rate = 0.001  # 학습률을 변경
    optimizer = Adam(learning_rate=learning_rate)

    # 모델 구성
    model = Sequential([
        GRU(64, input_shape=(X_train.shape[1], 1), return_sequences=True),
        GRU(32),
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

    # ReduceLROnPlateau 콜백: 검증 손실이 개선되지 않으면 학습률을 자동으로 감소
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=0.0001)

    # 모델 학습
    history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=50, batch_size=32, callbacks=[reduce_lr])
    print(f"Validation Accuracy: {max(history.history['val_accuracy'])}")
    return model, history

# --- 4. HAR 모델 학습 ---
def train_har_model(data_file, environment_label):
    data = pd.read_csv(data_file)
    data = data[data["Label"].apply(lambda x: x.startswith(environment_label))]
    X = data.drop(columns=["Label"]).values
    y = LabelEncoder().fit_transform(data["Label"])

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    model = Sequential([
        Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
        Dense(64, activation='relu'),
        Dense(len(np.unique(y)), activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=50, batch_size=32)
    print(f"Validation Accuracy: {max(history.history['val_accuracy'])}")
    return model

# --- 5. 모델 성능 시각화 ---
def plot_training_history(history):
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.legend()
    plt.title('Accuracy over epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.show()

    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.legend()
    plt.title('Loss over epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.show()

# --- 6. 예측 및 성능 평가 ---
def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    predicted_classes = np.argmax(predictions, axis=1)  # 다중 클래스 분류
    accuracy = accuracy_score(y_test, predicted_classes)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    cm = confusion_matrix(y_test, predicted_classes)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title("Confusion Matrix")
    plt.show()

# --- 실행 단계 ---
# 1. .pcap → CSV 변환
process_pcap_to_csv(pcap_folder="C:/Users/leejj/Desktop/Project", output_folder="C:/Users/leejj/Desktop/Project")

# 2. CSV 결합
combine_csv(input_folder="C:/Users/leejj/Desktop/Project", output_file="C:/Users/leejj/Desktop/Project/combined_data.csv")

# 3. LoS/NLoS 식별 모델 학습
los_nlos_model, los_nlos_history = train_los_nlos_model("C:/Users/leejj/Desktop/Project/combined_data.csv")

# 4. HAR 모델 학습 (LoS 환경)
los_har_model = train_har_model("C:/Users/leejj/Desktop/Project/combined_data.csv", environment_label="los")

# 5. HAR 모델 학습 (NLoS 환경)
nlos_har_model = train_har_model("C:/Users/leejj/Desktop/Project/combined_data.csv", environment_label="Nlos")

# 6. 데이터 분할 및 평가
data = pd.read_csv("C:/Users/leejj/Desktop/Project/combined_data.csv")
X = data.drop(columns=["Label"]).values
y = LabelEncoder().fit_transform(data["Label"].apply(lambda x: "NLoS" if x.startswith("Nlos") else "LoS"))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# LoS와 NLoS 데이터 분리
X_test_los = X_test[y_test == 0]  # LoS 환경
y_test_los = y_test[y_test == 0]

X_test_nlos = X_test[y_test == 1]  # NLoS 환경
y_test_nlos = y_test[y_test == 1]

# 모델 평가 (LoS 환경 모델 평가)
evaluate_model(los_har_model, X_test_los, y_test_los)

# 모델 평가 (NLoS 환경 모델 평가)
evaluate_model(nlos_har_model, X_test_nlos, y_test_nlos)