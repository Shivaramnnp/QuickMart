package com.shiva.quickMart.database

import androidx.lifecycle.LiveData
import androidx.room.*
import com.shiva.quickMart.models.CartItem

@Dao
interface CartDao {
    @Query("SELECT * FROM cart_items")
    fun getAllCartItems(): LiveData<List<CartItem>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertOrUpdate(cartItem: CartItem)

    @Delete
    suspend fun delete(cartItem: CartItem)

    @Query("DELETE FROM cart_items")
    suspend fun clearCart()
    
    @Query("SELECT SUM(quantity) FROM cart_items")
    fun getCartCount(): LiveData<Int>
}