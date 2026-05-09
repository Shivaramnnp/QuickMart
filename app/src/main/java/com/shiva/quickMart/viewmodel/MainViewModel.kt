package com.shiva.quickMart.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import com.shiva.quickMart.database.AppDatabase
import com.shiva.quickMart.models.CartItem
import com.shiva.quickMart.models.Product
import com.shiva.quickMart.repository.CartRepository
import kotlinx.coroutines.launch

class MainViewModel(application: Application) : AndroidViewModel(application) {
    private val repository: CartRepository
    val allCartItems: LiveData<List<CartItem>>
    val cartCount: LiveData<Int>

    private val _products = MutableLiveData<List<Product>>()
    val products: LiveData<List<Product>> = _products

    init {
        val cartDao = AppDatabase.getDatabase(application).cartDao()
        repository = CartRepository(cartDao)
        allCartItems = repository.allCartItems
        cartCount = repository.cartCount
        loadDummyProducts()
    }

    private fun loadDummyProducts() {
        _products.value = listOf(
            Product(1, "Apple", "Fruits", 120.0, "https://images.unsplash.com/photo-1560806887-1e4cd0b6fac6?auto=format&fit=crop&w=300&q=80"),
            Product(2, "Milk", "Dairy", 50.0, "https://images.unsplash.com/photo-1550583724-b2692b85b150?auto=format&fit=crop&w=300&q=80"),
            Product(3, "Chips", "Snacks", 30.0, "https://images.unsplash.com/photo-1566478989037-e924e50cb792?auto=format&fit=crop&w=300&q=80"),
            Product(4, "Bread", "Bakery", 40.0, "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=300&q=80"),
            Product(5, "Juice", "Beverages", 60.0, "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=300&q=80")
        )
    }

    fun searchProducts(query: String, category: String = "All") {
        val allProducts = listOf(
            Product(1, "Apple", "Fruits", 120.0, "https://images.unsplash.com/photo-1560806887-1e4cd0b6fac6?auto=format&fit=crop&w=300&q=80"),
            Product(2, "Milk", "Dairy", 50.0, "https://images.unsplash.com/photo-1550583724-b2692b85b150?auto=format&fit=crop&w=300&q=80"),
            Product(3, "Chips", "Snacks", 30.0, "https://images.unsplash.com/photo-1566478989037-e924e50cb792?auto=format&fit=crop&w=300&q=80"),
            Product(4, "Bread", "Bakery", 40.0, "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=300&q=80"),
            Product(5, "Juice", "Beverages", 60.0, "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=300&q=80")
        )
        
        var filtered = allProducts
        if (category != "All") {
            filtered = filtered.filter { it.category.equals(category, ignoreCase = true) }
        }
        if (query.isNotEmpty()) {
            filtered = filtered.filter { it.name.contains(query, ignoreCase = true) }
        }
        _products.value = filtered
    }

    fun updateCartItem(product: Product, quantity: Int) = viewModelScope.launch {
        repository.insertOrUpdate(CartItem(product.id, product.name, product.price, product.image, quantity))
    }

    fun updateCartItem(cartItem: CartItem, quantity: Int) = viewModelScope.launch {
        repository.insertOrUpdate(cartItem.copy(quantity = quantity))
    }

    fun clearCart() = viewModelScope.launch {
        repository.clearCart()
    }
}