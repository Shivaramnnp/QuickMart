package com.shiva.quickMart.models

data class Order(
    val orderId: String,
    val address: String,
    val paymentMethod: String,
    val totalAmount: Double
)