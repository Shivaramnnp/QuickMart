package com.shiva.quickMart.activities

import android.content.Intent
import android.os.Bundle
import android.view.View
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.shiva.quickMart.adapters.CartAdapter
import com.shiva.quickMart.databinding.ActivityCartBinding
import com.shiva.quickMart.viewmodel.MainViewModel

class CartActivity : AppCompatActivity() {
    private lateinit var binding: ActivityCartBinding
    private val viewModel: MainViewModel by viewModels()
    private lateinit var adapter: CartAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityCartBinding.inflate(layoutInflater)
        setContentView(binding.root)

        adapter = CartAdapter(emptyList()) { cartItem, newQuantity ->
            viewModel.updateCartItem(cartItem, newQuantity)
        }

        binding.rvCartItems.layoutManager = LinearLayoutManager(this)
        binding.rvCartItems.adapter = adapter

        viewModel.allCartItems.observe(this) { items ->
            adapter.updateItems(items)
            updateBillSummary(items)
            
            if (items.isEmpty()) {
                binding.llEmptyCart.visibility = View.VISIBLE
                binding.cvBillSummary.visibility = View.GONE
                binding.btnCheckout.visibility = View.GONE
            } else {
                binding.llEmptyCart.visibility = View.GONE
                binding.cvBillSummary.visibility = View.VISIBLE
                binding.btnCheckout.visibility = View.VISIBLE
            }
        }

        binding.btnCheckout.setOnClickListener {
            startActivity(Intent(this, CheckoutActivity::class.java))
        }
        
        binding.btnStartShopping.setOnClickListener {
            finish()
        }
    }

    private fun updateBillSummary(items: List<com.shiva.quickMart.models.CartItem>) {
        val itemTotal = items.sumOf { it.price * it.quantity }
        val deliveryCharge = if (itemTotal > 0) 30.0 else 0.0
        val grandTotal = itemTotal + deliveryCharge

        binding.tvItemTotal.text = "₹${itemTotal}"
        binding.tvDeliveryCharge.text = "₹${deliveryCharge}"
        binding.tvGrandTotal.text = "₹${grandTotal}"
    }
}