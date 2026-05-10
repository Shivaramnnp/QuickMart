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