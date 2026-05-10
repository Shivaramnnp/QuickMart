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