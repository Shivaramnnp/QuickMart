package com.shiva.quickMart.adapters

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.shiva.quickMart.databinding.ItemCartBinding
import com.shiva.quickMart.models.CartItem

class CartAdapter(
    private var cartItems: List<CartItem>,
    private val onQuantityChange: (CartItem, Int) -> Unit
) : RecyclerView.Adapter<CartAdapter.CartViewHolder>() {

    inner class CartViewHolder(val binding: ItemCartBinding) : RecyclerView.ViewHolder(binding.root)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): CartViewHolder {
        val binding = ItemCartBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return CartViewHolder(binding)
    }

    override fun onBindViewHolder(holder: CartViewHolder, position: Int) {
        val item = cartItems[position]
        holder.binding.apply {
            tvCartProductName.text = item.name
            tvCartProductPrice.text = "₹${item.price}"
            tvQuantity.text = item.quantity.toString()
            Glide.with(ivCartProduct.context).load(item.image).into(ivCartProduct)

            btnIncrease.setOnClickListener { onQuantityChange(item, item.quantity + 1) }
            btnDecrease.setOnClickListener { onQuantityChange(item, item.quantity - 1) }
        }
    }

    override fun getItemCount() = cartItems.size

    fun updateItems(newItems: List<CartItem>) {
        cartItems = newItems
        notifyDataSetChanged()
    }
}