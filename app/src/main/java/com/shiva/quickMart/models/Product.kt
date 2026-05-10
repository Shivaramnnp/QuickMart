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