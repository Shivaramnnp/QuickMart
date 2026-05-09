import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip())

# Models
write_file('app/src/main/java/com/shiva/quickMart/models/Product.kt', """
package com.shiva.quickMart.models

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.io.Serializable

@Entity(tableName = "products")
data class Product(
    @PrimaryKey val id: Int,
    val name: String,
    val category: String,
    val price: Double,
    val image: String,
    var quantity: Int = 0
) : Serializable
""")

write_file('app/src/main/java/com/shiva/quickMart/models/CartItem.kt', """
package com.shiva.quickMart.models

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "cart_items")
data class CartItem(
    @PrimaryKey val productId: Int,
    val name: String,
    val price: Double,
    val image: String,
    var quantity: Int
)
""")

write_file('app/src/main/java/com/shiva/quickMart/models/Order.kt', """
package com.shiva.quickMart.models

data class Order(
    val orderId: String,
    val address: String,
    val paymentMethod: String,
    val totalAmount: Double
)
""")

# Database
write_file('app/src/main/java/com/shiva/quickMart/database/CartDao.kt', """
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
""")

write_file('app/src/main/java/com/shiva/quickMart/database/AppDatabase.kt', """
package com.shiva.quickMart.database

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import com.shiva.quickMart.models.CartItem
import com.shiva.quickMart.models.Product

@Database(entities = [CartItem::class, Product::class], version = 1, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun cartDao(): CartDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getDatabase(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "quickmart_db"
                ).build()
                INSTANCE = instance
                instance
            }
        }
    }
}
""")

# Repository
write_file('app/src/main/java/com/shiva/quickMart/repository/CartRepository.kt', """
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
""")

# ViewModel
write_file('app/src/main/java/com/shiva/quickMart/viewmodel/MainViewModel.kt', """
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
""")

print("Kotlin files written.")
