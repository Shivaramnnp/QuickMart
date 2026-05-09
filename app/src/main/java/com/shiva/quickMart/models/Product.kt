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