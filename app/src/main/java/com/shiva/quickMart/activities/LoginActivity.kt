package com.shiva.quickMart.activities

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.shiva.quickMart.databinding.ActivityLoginBinding

class LoginActivity : AppCompatActivity() {
    private lateinit var binding: ActivityLoginBinding
    private var generatedOtp: String = "1234"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityLoginBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.btnSendOtp.setOnClickListener {
            val phone = binding.etPhone.text.toString()
            if (phone.length == 10) {
                Toast.makeText(this, "OTP Sent", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "Enter valid 10-digit number", Toast.LENGTH_SHORT).show()
            }
        }

        binding.btnVerifyOtp.setOnClickListener {
            val phone = binding.etPhone.text.toString()
            val otp = binding.etOtp.text.toString()
            if (phone.length == 10 && otp == generatedOtp) {
                startActivity(Intent(this, HomeActivity::class.java))
                finish()
            } else {
                Toast.makeText(this, "Invalid OTP or Phone Number", Toast.LENGTH_SHORT).show()
            }
        }
    }
}