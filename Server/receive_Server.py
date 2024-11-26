import socket
import time
import os
import csv

# 서버 설정
HOST = "0.0.0.0"  # 모든 네트워크 인터페이스에서 연결 허용
PORT = 8080       # 앱과 동일한 포트 사용

# CSV 파일에서 데이터 읽기
def read_csv_file(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        data = [row for row in csvreader]  # CSV의 모든 행을 리스트로 읽어옴
    return data

# 데이터 스트리밍 서버
def start_server(csv_folder):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connected to {client_address}")
            try:
                # 폴더 내 모든 CSV 파일 목록 가져오기
                csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]
                if not csv_files:
                    print("No CSV files found in the folder.")
                    continue

                # 각 파일을 클라이언트에 전송
                for file_name in csv_files:
                    file_path = os.path.join(csv_folder, file_name)
                    print(f"Sending file: {file_path}")
                    
                    # 파일 이름 전송 (구분용 태그 추가)
                    client_socket.sendall(f"FILE_START:{file_name}\n".encode("utf-8"))
                    
                    csv_data = read_csv_file(file_path)
                    for row in csv_data:
                        data_line = ",".join(row)
                        client_socket.sendall(data_line.encode("utf-8"))
                        client_socket.sendall(b"\n")  # 줄바꿈 추가
                        time.sleep(0.1)  # 데이터 전송 간격

                    # 파일 전송 완료 알림
                    client_socket.sendall("FILE_END\n".encode("utf-8"))

                print("All files sent successfully.")
            except Exception as e:
                print(f"Error during transmission: {e}")
            finally:
                client_socket.close()

if __name__ == "__main__":
    csv_folder = "C:/Users/leejj/Desktop/Project/a"  # CSV 파일이 저장된 폴더 경로
    start_server(csv_folder)
