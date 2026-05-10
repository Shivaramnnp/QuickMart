package com.shiva.quickMart.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.MediatorLiveData
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

    private val masterProducts = listOf(
        // Fruits
        Product(1, "Apple", "Fruits", 120.0, "https://unsplash.com/photos/fresh-red-apples-in-the-wooden-box-on-black-background-top-view-9OrF6J9AcVA"),
        Product(2, "Banana", "Fruits", 50.0, "https://images.unsplash.com/photo-1528825871115-3581a5387919?auto=format&fit=crop&w=300&q=80"),
        Product(3, "Orange", "Fruits", 80.0, "https://images.unsplash.com/photo-1549888834-3ec93abae044?auto=format&fit=crop&w=300&q=80"),
        Product(4, "Grapes", "Fruits", 90.0, "https://images.unsplash.com/photo-1537640538966-79f369143f8f?auto=format&fit=crop&w=300&q=80"),
        
        // Dairy
        Product(5, "Milk", "Dairy", 60.0, "https://images.unsplash.com/photo-1550583724-b2692b85b150?auto=format&fit=crop&w=300&q=80"),
        Product(6, "Cheese", "Dairy", 150.0, "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?auto=format&fit=crop&w=300&q=80"),
        Product(7, "Butter", "Dairy", 200.0, "https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?auto=format&fit=crop&w=300&q=80"),
        Product(8, "Yogurt", "Dairy", 45.0, "https://images.unsplash.com/photo-1564149504298-00c351fd7f16?auto=format&fit=crop&w=300&q=80"),

        // Snacks
        Product(9, "Potato Chips", "Snacks", 30.0, "https://images.unsplash.com/photo-1621852004158-f3bc188ace2d?auto=format&fit=crop&w=300&q=80"),
        Product(10, "Nachos", "Snacks", 85.0, "https://images.unsplash.com/photo-1513456852971-30c0b8199d4d?auto=format&fit=crop&w=300&q=80"),
        Product(11, "Popcorn", "Snacks", 50.0, "https://images.unsplash.com/photo-1585653040134-4538ec2f004f?auto=format&fit=crop&w=300&q=80"),
        Product(12, "Cookies", "Snacks", 60.0, "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?auto=format&fit=crop&w=300&q=80"),

        // Beverages
        Product(13, "Orange Juice", "Beverages", 110.0, "https://images.unsplash.com/photo-1600271886742-f049cd451bba?auto=format&fit=crop&w=300&q=80"),
        Product(14, "Cola", "Beverages", 40.0, "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=300&q=80"),
        Product(15, "Energy Drink", "Beverages", 120.0, "https://images.unsplash.com/photo-1622543925917-763c34d1a86e?auto=format&fit=crop&w=300&q=80"),
        
        // Bakery
        Product(16, "Whole Wheat Bread", "Bakery", 45.0, "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=300&q=80"),
        Product(17, "Croissant", "Bakery", 60.0, "https://images.unsplash.com/photo-1530610476181-d83430b64dcb?auto=format&fit=crop&w=300&q=80"),
        Product(18, "Muffins", "Bakery", 90.0, "https://images.unsplash.com/photo-1607958996333-41aef7caefaa?auto=format&fit=crop&w=300&q=80")
    )

    private val _filteredProducts = MutableLiveData<List<Product>>()
    val products = MediatorLiveData<List<Product>>()

    init {
        val cartDao = AppDatabase.getDatabase(application).cartDao()
        repository = CartRepository(cartDao)
        allCartItems = repository.allCartItems
        cartCount = repository.cartCount

        products.addSource(_filteredProducts) { filteredList ->
            val cartList = allCartItems.value ?: emptyList()
            products.value = mapQuantities(filteredList, cartList)
        }
        
        products.addSource(allCartItems) { cartList ->
            val filteredList = _filteredProducts.value ?: masterProducts
            products.value = mapQuantities(filteredList, cartList)
        }

        loadDummyProducts()
    }
    
    private fun mapQuantities(prodList: List<Product>, cartList: List<CartItem>): List<Product> {
        val cartMap = cartList.associateBy { it.productId }
        return prodList.map { p -> 
            p.copy(quantity = cartMap[p.id]?.quantity ?: 0)
        }
    }

    private fun loadDummyProducts() {
        _filteredProducts.value = masterProducts
    }

    fun searchProducts(query: String, category: String = "All") {
        var filtered = masterProducts
        if (category != "All") {
            filtered = filtered.filter { it.category.equals(category, ignoreCase = true) }
        }
        if (query.isNotEmpty()) {
            filtered = filtered.filter { it.name.contains(query, ignoreCase = true) }
        }
        _filteredProducts.value = filtered
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