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