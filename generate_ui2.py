import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip())

# Activities part 2
write_file('app/src/main/java/com/shiva/quickMart/activities/HomeActivity.kt', """
package com.shiva.quickMart.activities

import android.content.Intent
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.View
import android.widget.Toast
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.GridLayoutManager
import com.shiva.quickMart.adapters.ProductAdapter
import com.shiva.quickMart.databinding.ActivityHomeBinding
import com.shiva.quickMart.viewmodel.MainViewModel

class HomeActivity : AppCompatActivity() {
    private lateinit var binding: ActivityHomeBinding
    private val viewModel: MainViewModel by viewModels()
    private lateinit var adapter: ProductAdapter
    private var currentCategory = "All"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityHomeBinding.inflate(layoutInflater)
        setContentView(binding.root)

        adapter = ProductAdapter(emptyList()) { product ->
            viewModel.updateCartItem(product, product.quantity + 1)
            Toast.makeText(this, "${product.name} added to cart", Toast.LENGTH_SHORT).show()
        }

        binding.rvProducts.layoutManager = GridLayoutManager(this, 2)
        binding.rvProducts.adapter = adapter

        viewModel.products.observe(this) { products ->
            adapter.updateProducts(products)
        }

        viewModel.cartCount.observe(this) { count ->
            binding.tvCartCount.text = (count ?: 0).toString()
        }

        binding.etSearch.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                viewModel.searchProducts(s.toString(), currentCategory)
            }
            override fun afterTextChanged(s: Editable?) {}
        })

        binding.chipGroupCategories.setOnCheckedStateChangeListener { group, checkedIds ->
            if (checkedIds.isNotEmpty()) {
                val selectedChipId = checkedIds[0]
                currentCategory = when (selectedChipId) {
                    binding.chipFruits.id -> "Fruits"
                    binding.chipDairy.id -> "Dairy"
                    binding.chipSnacks.id -> "Snacks"
                    binding.chipBeverages.id -> "Beverages"
                    binding.chipBakery.id -> "Bakery"
                    else -> "All"
                }
                viewModel.searchProducts(binding.etSearch.text.toString(), currentCategory)
            } else {
                currentCategory = "All"
                viewModel.searchProducts(binding.etSearch.text.toString(), currentCategory)
            }
        }

        binding.fabCart.setOnClickListener {
            startActivity(Intent(this, CartActivity::class.java))
        }
    }
}
""")

write_file('app/src/main/java/com/shiva/quickMart/activities/CartActivity.kt', """
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
""")

write_file('app/src/main/java/com/shiva/quickMart/activities/CheckoutActivity.kt', """
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
""")

write_file('app/src/main/java/com/shiva/quickMart/activities/OrderSuccessActivity.kt', """
package com.shiva.quickMart.activities

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.shiva.quickMart.databinding.ActivityOrderSuccessBinding

class OrderSuccessActivity : AppCompatActivity() {
    private lateinit var binding: ActivityOrderSuccessBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityOrderSuccessBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        binding.tvOrderId.text = "Order ID: QM1024"
        binding.tvDeliveryTime.text = "Estimated delivery: 15–20 mins"

        binding.btnContinueShopping.setOnClickListener {
            startActivity(Intent(this, HomeActivity::class.java))
            finishAffinity()
        }
    }
}
""")

print("Activities 2 written.")
