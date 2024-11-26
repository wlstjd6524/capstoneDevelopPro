package com.example.myapplication

import java.io.InputStream
import java.io.BufferedReader
import java.io.InputStreamReader
import java.net.Socket
import java.nio.ByteBuffer
import java.nio.ByteOrder
import org.tensorflow.lite.Interpreter
import android.app.Notification
import android.app.NotificationManager
import android.content.Context
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.NotificationCompat
import java.util.concurrent.Executors
import java.text.SimpleDateFormat
import java.util.Locale
import android.util.Log
import android.os.Build
import android.app.NotificationChannel
import androidx.core.content.ContextCompat
import androidx.core.app.ActivityCompat
import android.content.pm.PackageManager
import android.Manifest




class MainActivity : AppCompatActivity() {

    private lateinit var handler: Handler
    private var lastMoveTime: Long = System.currentTimeMillis()
    private val movementThreshold: Long = 3600000 // 1시간 동안 움직임이 없으면 알림
    private var model: MyMLModel? = null // 머신러닝 모델을 사용할 변수

    private var isServerConnected = false
    private lateinit var socket: Socket
    private lateinit var inputStream: InputStream
    private lateinit var reader: BufferedReader

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        handler = Handler(Looper.getMainLooper())

        // TensorFlow Lite 모델 로드
        model = loadMachineLearningModel()

        // 권한 요청 (Android 13 이상)
        requestNotificationPermission()

        // 버튼 클릭 이벤트 설정
        val connectButton: Button = findViewById(R.id.button1)
        connectButton.setOnClickListener {
            if (!isServerConnected) {
                connectButton.text = "연결 중..."
                startNetworkDataProcessing("192.168.219.100", 8080, connectButton)
            }
        }

        // 움직임이 없는 경우 알림 보내기 (주기적으로 체크)
        startMovementCheckTimer()

        // 알림 채널 생성
        createNotificationChannel()
    }

    private fun requestNotificationPermission() {
        // Android 13 (API 33) 이상에서 알림 권한 요청
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS)
                != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(
                    this,
                    arrayOf(Manifest.permission.POST_NOTIFICATIONS),
                    1 // 권한 요청 코드
                )
            }
        }
    }

    //createNotificationChannel 함수로 채널 생성 후 알림을 보내는 코드
    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val name = "Movement Notifications"
            val descriptionText = "Notifies when no movement is detected"
            val importance = NotificationManager.IMPORTANCE_HIGH
            val channel = NotificationChannel("movement_channel", name, importance).apply {
                description = descriptionText
            }
            val notificationManager: NotificationManager =
                getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(channel)
        }
    }


    // 네트워크 데이터를 수신하는 함수
    private fun startNetworkDataProcessing(host: String, port: Int, button: Button) {
        val executor = Executors.newSingleThreadExecutor()
        executor.execute {
            try {
                socket = Socket(host, port) // 서버에 연결
                inputStream = socket.getInputStream()
                reader = BufferedReader(InputStreamReader(inputStream))

                isServerConnected = true
                runOnUiThread {
                    button.text = "연결 완료"
                    val textView: TextView = findViewById(R.id.text1)
                    textView.text = "서버 연결 상태 : 연결 됨."

                }

                var line: String?
                while (reader.readLine().also { line = it } != null) {
                    line?.let { rawData ->
                        processNetworkData(rawData)
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
                runOnUiThread {
                    button.text = "연결 중."
                }
            }
        }
    }


    // TensorFlow Lite 모델 로드 함수
    private fun loadMachineLearningModel(): MyMLModel? {
        return try {
            val assetManager = assets
            val modelFileDescriptor = assetManager.openFd("los_nlos_model.tflite")
            val inputStream = modelFileDescriptor.createInputStream()
            val byteBuffer = convertInputStreamToByteBuffer(inputStream, modelFileDescriptor.length)

            val interpreter = Interpreter(byteBuffer) // TensorFlow Lite 인터프리터
            MyMLModel(interpreter) // MyMLModel 객체 반환
        } catch (e: Exception) {
            e.printStackTrace()
            null
        }
    }

    private fun convertInputStreamToByteBuffer(inputStream: InputStream, fileLength: Long): ByteBuffer {
        val byteBuffer = ByteBuffer.allocateDirect(fileLength.toInt())
        byteBuffer.order(ByteOrder.nativeOrder())

        val bytes = ByteArray(fileLength.toInt())
        inputStream.read(bytes)
        byteBuffer.put(bytes)
        byteBuffer.rewind()

        return byteBuffer
    }

    // 네트워크 데이터를 수신하는 함수
    private fun startNetworkDataProcessing(host: String, port: Int) {
        val executor = Executors.newSingleThreadExecutor()
        executor.execute {
            try {
                val socket = Socket(host, port) // 서버에 연결
                val inputStream = socket.getInputStream()
                val reader = BufferedReader(InputStreamReader(inputStream))

                var line: String?
                while (reader.readLine().also { line = it } != null) {
                    line?.let { rawData ->
                        processNetworkData(rawData)
                    }
                }

                reader.close()
                socket.close()
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    // 수신된 네트워크 데이터를 처리하는 함수
    private fun processNetworkData(rawData: String) {
        try {
            Log.d("NetworkData", "Received data: $rawData")  // 여기서 로그를 출력합니다.
            // 수신된 데이터를 CSV로 파싱
            val csiData = rawData.split(",").map { it.trim().toFloat() }
            Log.d("ParsedData", "Parsed data: $csiData")

            // 데이터를 분석
            runOnUiThread {
                analyzeRealTimeData(csiData)
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    // 실시간 데이터를 분석하는 함수

    private fun analyzeRealTimeData(data: List<Float>) {
        // 예시: 머신러닝 모델을 사용하여 실시간 데이터 패턴 분석
        val prediction = predictMovementPattern(data)

        // 예측된 결과가 움직임을 나타낸다면, 움직임 시간을 갱신
        if (prediction) {
            lastMoveTime = System.currentTimeMillis()
        }
    }

    // 머신러닝 모델을 사용하여 예측하는 함수
    private fun predictMovementPattern(data: List<Float>): Boolean {
        // 모델을 사용하여 실시간 데이터로 예측 수행
        return model?.predict(data) ?: false // 예측 결과 (움직임/없음)
    }

    // 움직임을 감지하지 않으면 알림 보내기
    private fun startMovementCheckTimer() {
        handler.postDelayed(object : Runnable {
            override fun run() {
                val currentTime = System.currentTimeMillis()
                if (currentTime - lastMoveTime >= movementThreshold) {
                    sendNoMovementNotification()
                }
                handler.postDelayed(this, 3600000) // 1시간 마다 체크
            }
        }, 3600000)
    }

    // 알림 보내기
    private fun sendNoMovementNotification() {
        val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        val notification = NotificationCompat.Builder(this, "movement_channel")
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .setContentTitle("알림!")
            .setContentText("1시간 동안 움직임이 감지되지 않았습니다. 확인해 주세요.")
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .build()

        notificationManager.notify(1, notification)
    }
}

class MyMLModel(private val interpreter: Interpreter) {

    // 모델을 사용하여 예측하는 함수
    fun predict(data: List<Float>): Boolean {
        // 예측을 위한 입력 데이터를 준비
        val inputBuffer = convertDataToByteBuffer(data)

        // 예측 결과를 저장할 변수
        val outputBuffer = ByteBuffer.allocateDirect(4) // 예시: 1개의 예측 값 (boolean 형태로 처리)
        outputBuffer.order(ByteOrder.nativeOrder())

        // 모델 예측 수행
        interpreter.run(inputBuffer, outputBuffer)

        // 예측 결과 가져오기
        outputBuffer.rewind()
        val prediction = outputBuffer.float

        // 예측 값이 일정 기준을 넘으면 움직임이 있다고 간주
        return prediction > 0.65f // 예시: 예측값이 0.5 이상이면 움직임 있음
    }

    // 데이터를 ByteBuffer로 변환하는 함수
    private fun convertDataToByteBuffer(data: List<Float>): ByteBuffer {
        val buffer = ByteBuffer.allocateDirect(data.size * 4) // 각 Float은 4바이트
        buffer.order(ByteOrder.nativeOrder())

        for (value in data) {
            buffer.putFloat(value)
        }

        buffer.rewind()
        return buffer
    }

    // 모델을 닫을 때 호출하는 함수
    fun close() {
        interpreter.close()
    }
}