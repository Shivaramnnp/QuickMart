package com.shiva.quickMart.activities

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import com.shiva.quickMart.databinding.ActivityCheckoutBinding
import com.shiva.quickMart.viewmodel.MainViewModel

class CheckoutActivity : AppCompatActivity() {
    private lateinit var binding: ActivityCheckoutBinding
    private val viewModel: MainViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityCheckoutBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.btnPlaceOrder.setOnClickListener {
            val address = binding.etAddress.text.toString()
            val paymentSelected = binding.rgPayment.checkedRadioButtonId != -1
            
            if (address.isEmpty()) {
                Toast.makeText(this, "Please enter an address", Toast.LENGTH_SHORT).show()
            } else if (!paymentSelected) {
                Toast.makeText(this, "Please select a payment method", Toast.LENGTH_SHORT).show()
            } else {
                viewModel.clearCart()
                startActivity(Intent(this, OrderSuccessActivity::class.java))
                finishAffinity()
            }
        }
    }
}