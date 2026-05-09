package com.shiva.quickMart.repository

import androidx.lifecycle.LiveData
import com.shiva.quickMart.database.CartDao
import com.shiva.quickMart.models.CartItem

class CartRepository(private val cartDao: CartDao) {
    val allCartItems: LiveData<List<CartItem>> = cartDao.getAllCartItems()
    val cartCount: LiveData<Int> = cartDao.getCartCount()

    suspend fun insertOrUpdate(cartItem: CartItem) {
        if (cartItem.quantity > 0) {
            cartDao.insertOrUpdate(cartItem)
        } else {
            cartDao.delete(cartItem)
        }
    }

    suspend fun clearCart() {
        cartDao.clearCart()
    }
}