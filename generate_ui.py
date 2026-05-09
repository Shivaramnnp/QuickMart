import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip())

# Adapters
write_file('app/src/main/java/com/shiva/quickMart/adapters/ProductAdapter.kt', """
package com.shiva.quickMart.adapters

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.shiva.quickMart.databinding.ItemProductBinding
import com.shiva.quickMart.models.Product

class ProductAdapter(
    private var products: List<Product>,
    private val onAddToCart: (Product) -> Unit
) : RecyclerView.Adapter<ProductAdapter.ProductViewHolder>() {

    inner class ProductViewHolder(val binding: ItemProductBinding) : RecyclerView.ViewHolder(binding.root)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ProductViewHolder {
        val binding = ItemProductBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return ProductViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ProductViewHolder, position: Int) {
        val product = products[position]
        holder.binding.apply {
            tvProductName.text = product.name
            tvProductCategory.text = product.category
            tvProductPrice.text = "₹${product.price}"
            Glide.with(ivProduct.context).load(product.image).into(ivProduct)
            
            btnAddToCart.setOnClickListener {
                onAddToCart(product)
            }
        }
    }

    override fun getItemCount() = products.size

    fun updateProducts(newProducts: List<Product>) {
        products = newProducts
        notifyDataSetChanged()
    }
}
""")

write_file('app/src/main/java/com/shiva/quickMart/adapters/CartAdapter.kt', """
package com.shiva.quickMart.adapters

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.shiva.quickMart.databinding.ItemCartBinding
import com.shiva.quickMart.models.CartItem

class CartAdapter(
    private var cartItems: List<CartItem>,
    private val onQuantityChange: (CartItem, Int) -> Unit
) : RecyclerView.Adapter<CartAdapter.CartViewHolder>() {

    inner class CartViewHolder(val binding: ItemCartBinding) : RecyclerView.ViewHolder(binding.root)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): CartViewHolder {
        val binding = ItemCartBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return CartViewHolder(binding)
    }

    override fun onBindViewHolder(holder: CartViewHolder, position: Int) {
        val item = cartItems[position]
        holder.binding.apply {
            tvCartProductName.text = item.name
            tvCartProductPrice.text = "₹${item.price}"
            tvQuantity.text = item.quantity.toString()
            Glide.with(ivCartProduct.context).load(item.image).into(ivCartProduct)

            btnIncrease.setOnClickListener { onQuantityChange(item, item.quantity + 1) }
            btnDecrease.setOnClickListener { onQuantityChange(item, item.quantity - 1) }
        }
    }

    override fun getItemCount() = cartItems.size

    fun updateItems(newItems: List<CartItem>) {
        cartItems = newItems
        notifyDataSetChanged()
    }
}
""")

write_file('app/src/main/java/com/shiva/quickMart/activities/LoginActivity.kt', """
package com.shiva.quickMart.activities

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.shiva.quickMart.databinding.ActivityLoginBinding

class LoginActivity : AppCompatActivity() {
    private lateinit binding: ActivityLoginBinding
    private var generatedOtp: String = "1234"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityLoginBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.btnSendOtp.setOnClickListener {
            val phone = binding.etPhone.text.toString()
            if (phone.length == 10) {
                Toast.makeText(this, "OTP Sent: 1234", Toast.LENGTH_SHORT).show()
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
""")

print("Activities 1 written.")
