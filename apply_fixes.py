import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip())

# Task 1 & 2: Fix Product Entity and AppDatabase
write_file('app/src/main/java/com/shiva/quickMart/models/Product.kt', """
package com.shiva.quickMart.models

import java.io.Serializable

data class Product(
    val id: Int,
    val name: String,
    val category: String,
    val price: Double,
    val image: String,
    var quantity: Int = 0
) : Serializable
""")

write_file('app/src/main/java/com/shiva/quickMart/database/AppDatabase.kt', """
package com.shiva.quickMart.database

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import com.shiva.quickMart.models.CartItem

@Database(entities = [CartItem::class], version = 1, exportSchema = false)
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

# Task 3: Refactor MainViewModel with 15+ products and MediatorLiveData
write_file('app/src/main/java/com/shiva/quickMart/viewmodel/MainViewModel.kt', """
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
        Product(1, "Apple", "Fruits", 120.0, "https://images.unsplash.com/photo-1560806887-1e4cd0b6fac6?auto=format&fit=crop&w=300&q=80"),
        Product(2, "Banana", "Fruits", 50.0, "https://images.unsplash.com/photo-1528825871115-3581a5387919?auto=format&fit=crop&w=300&q=80"),
        Product(3, "Orange", "Fruits", 80.0, "https://images.unsplash.com/photo-1549888834-3ec93abae044?auto=format&fit=crop&w=300&q=80"),
        Product(4, "Grapes", "Fruits", 90.0, "https://images.unsplash.com/photo-1537640538966-79f369143f8f?auto=format&fit=crop&w=300&q=80"),
        
        // Dairy
        Product(5, "Milk", "Dairy", 60.0, "https://images.unsplash.com/photo-1550583724-b2692b85b150?auto=format&fit=crop&w=300&q=80"),
        Product(6, "Cheese", "Dairy", 150.0, "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?auto=format&fit=crop&w=300&q=80"),
        Product(7, "Butter", "Dairy", 200.0, "https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?auto=format&fit=crop&w=300&q=80"),
        Product(8, "Yogurt", "Dairy", 45.0, "https://images.unsplash.com/photo-1564149504298-00c351fd7f16?auto=format&fit=crop&w=300&q=80"),

        // Snacks
        Product(9, "Potato Chips", "Snacks", 30.0, "https://images.unsplash.com/photo-1566478989037-e924e50cb792?auto=format&fit=crop&w=300&q=80"),
        Product(10, "Nachos", "Snacks", 85.0, "https://images.unsplash.com/photo-1513456852971-30c0b8199d4d?auto=format&fit=crop&w=300&q=80"),
        Product(11, "Popcorn", "Snacks", 50.0, "https://images.unsplash.com/photo-1572804013309-8c9959d0e2db?auto=format&fit=crop&w=300&q=80"),
        Product(12, "Cookies", "Snacks", 60.0, "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?auto=format&fit=crop&w=300&q=80"),

        // Beverages
        Product(13, "Orange Juice", "Beverages", 110.0, "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=300&q=80"),
        Product(14, "Cola", "Beverages", 40.0, "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=300&q=80"),
        Product(15, "Energy Drink", "Beverages", 120.0, "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=300&q=80"),
        
        // Bakery
        Product(16, "Whole Wheat Bread", "Bakery", 45.0, "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=300&q=80"),
        Product(17, "Croissant", "Bakery", 60.0, "https://images.unsplash.com/photo-1555507036-ab1e4006aa24?auto=format&fit=crop&w=300&q=80"),
        Product(18, "Muffins", "Bakery", 90.0, "https://images.unsplash.com/photo-1557925923-b6dc240a2a53?auto=format&fit=crop&w=300&q=80")
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
""")

# Task 4 & 6 & 11: DiffUtil + Price format + Quantity UI
write_file('app/src/main/java/com/shiva/quickMart/adapters/ProductAdapter.kt', """
package com.shiva.quickMart.adapters

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.shiva.quickMart.databinding.ItemProductBinding
import com.shiva.quickMart.models.Product

class ProductAdapter(
    private val onQuantityChange: (Product, Int) -> Unit
) : ListAdapter<Product, ProductAdapter.ProductViewHolder>(ProductDiffCallback()) {

    inner class ProductViewHolder(val binding: ItemProductBinding) : RecyclerView.ViewHolder(binding.root)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ProductViewHolder {
        val binding = ItemProductBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return ProductViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ProductViewHolder, position: Int) {
        val product = getItem(position)
        holder.binding.apply {
            tvProductName.text = product.name
            tvProductCategory.text = product.category
            tvProductPrice.text = "₹${"%.0f".format(product.price)}"
            Glide.with(ivProduct.context).load(product.image).into(ivProduct)
            
            if (product.quantity > 0) {
                btnAddToCart.visibility = View.GONE
                llQuantityControl.visibility = View.VISIBLE
                tvQuantity.text = product.quantity.toString()
            } else {
                btnAddToCart.visibility = View.VISIBLE
                llQuantityControl.visibility = View.GONE
            }

            btnAddToCart.setOnClickListener {
                onQuantityChange(product, 1)
            }
            btnIncrease.setOnClickListener {
                onQuantityChange(product, product.quantity + 1)
            }
            btnDecrease.setOnClickListener {
                onQuantityChange(product, product.quantity - 1)
            }
        }
    }
}

class ProductDiffCallback : DiffUtil.ItemCallback<Product>() {
    override fun areItemsTheSame(oldItem: Product, newItem: Product): Boolean {
        return oldItem.id == newItem.id
    }

    override fun areContentsTheSame(oldItem: Product, newItem: Product): Boolean {
        return oldItem == newItem
    }
}
""")

write_file('app/src/main/java/com/shiva/quickMart/adapters/CartAdapter.kt', """
package com.shiva.quickMart.adapters

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.shiva.quickMart.databinding.ItemCartBinding
import com.shiva.quickMart.models.CartItem

class CartAdapter(
    private val onQuantityChange: (CartItem, Int) -> Unit
) : ListAdapter<CartItem, CartAdapter.CartViewHolder>(CartDiffCallback()) {

    inner class CartViewHolder(val binding: ItemCartBinding) : RecyclerView.ViewHolder(binding.root)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): CartViewHolder {
        val binding = ItemCartBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return CartViewHolder(binding)
    }

    override fun onBindViewHolder(holder: CartViewHolder, position: Int) {
        val item = getItem(position)
        holder.binding.apply {
            tvCartProductName.text = item.name
            tvCartProductPrice.text = "₹${"%.0f".format(item.price)}"
            tvQuantity.text = item.quantity.toString()
            Glide.with(ivCartProduct.context).load(item.image).into(ivCartProduct)

            btnIncrease.setOnClickListener { onQuantityChange(item, item.quantity + 1) }
            btnDecrease.setOnClickListener { onQuantityChange(item, item.quantity - 1) }
        }
    }
}

class CartDiffCallback : DiffUtil.ItemCallback<CartItem>() {
    override fun areItemsTheSame(oldItem: CartItem, newItem: CartItem): Boolean {
        return oldItem.productId == newItem.productId
    }

    override fun areContentsTheSame(oldItem: CartItem, newItem: CartItem): Boolean {
        return oldItem == newItem
    }
}
""")

# Task 5: Dynamic Order ID
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
        
        val orderId = System.currentTimeMillis() % 100000
        binding.tvOrderId.text = "Order ID: QM${orderId}"
        binding.tvDeliveryTime.text = "Estimated delivery: 15–20 mins"

        binding.btnContinueShopping.setOnClickListener {
            startActivity(Intent(this, HomeActivity::class.java))
            finishAffinity()
        }
    }
}
""")

# Refactor HomeActivity and CartActivity for ListAdapter
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

        adapter = ProductAdapter { product, newQuantity ->
            viewModel.updateCartItem(product, newQuantity)
        }

        binding.rvProducts.layoutManager = GridLayoutManager(this, 2)
        binding.rvProducts.adapter = adapter

        viewModel.products.observe(this) { products ->
            adapter.submitList(products)
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

        adapter = CartAdapter { cartItem, newQuantity ->
            viewModel.updateCartItem(cartItem, newQuantity)
        }

        binding.rvCartItems.layoutManager = LinearLayoutManager(this)
        binding.rvCartItems.adapter = adapter

        viewModel.allCartItems.observe(this) { items ->
            adapter.submitList(items)
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

        binding.tvItemTotal.text = "₹${"%.0f".format(itemTotal)}"
        binding.tvDeliveryCharge.text = "₹${"%.0f".format(deliveryCharge)}"
        binding.tvGrandTotal.text = "₹${"%.0f".format(grandTotal)}"
    }
}
""")

print("Done generating fix files!")
