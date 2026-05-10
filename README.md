# QuickMart 🛒

QuickMart is a lightweight, Blinkit-style grocery delivery Android application focused on providing a smooth and user-friendly shopping experience. This application demonstrates fundamental Android development concepts including MVVM architecture, RecyclerView, Room Database, ViewBinding, and clean UI implementation using Kotlin and XML.

## Features ✨
* **Login / OTP Verification**: Secure entry to the app using mobile number and (dummy) OTP verification (OTP: 1234).
* **Product Browsing**: Clean and modern UI for viewing a catalog of available groceries.
* **Search and Filter**: Instantly search for products or filter them by category (Fruits, Dairy, Snacks, etc.).
* **Cart Management**: Add products to cart, manage quantities seamlessly, and view dynamic bill summaries.
* **Local Persistence**: Products and cart items are stored locally using Room Database for offline resilience and persistence across sessions.
* **Checkout & Order Placement**: Choose payment options (COD or Online) and input a delivery address.
* **Order Success**: View estimated delivery time and order confirmation details.

## Tech Stack 🛠
* **Language**: Kotlin
* **UI**: XML Layouts, Material Design Components
* **Architecture**: MVVM (Model-View-ViewModel) pattern
* **Local Database**: Room Database
* **Asynchronous Operations**: Kotlin Coroutines & ViewModel Scope
* **Image Loading**: Glide
* **Other Components**: RecyclerView, ViewBinding, LiveData

## Screenshots & Demo 📱
*You can find the `quickmart_demo.mp4` screen recording in the project root to view the application in action!*

![App Demo](quickmart_demo.mp4)

## Installation Steps 🚀
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/shivarampatel/QuickMart.git
   ```
2. Open the project in **Android Studio**.
3. Allow Gradle to sync and download all necessary dependencies.
4. Run the app on an Android Emulator or a physical device via USB debugging.

## Folder Structure 📂
```
app/src/main/java/com/shiva/quickMart/
  ├── activities/    # UI controllers (Login, Home, Cart, Checkout, Success)
  ├── adapters/      # RecyclerView adapters for products and cart items
  ├── models/        # Data classes (Product, CartItem, Order)
  ├── database/      # Room database configuration and DAOs
  ├── repository/    # Data layer handling database operations
  ├── viewmodel/     # ViewModel handling business logic and UI state
```

## Future Improvements 🔮
* Integration with Firebase Authentication for real user verification.
* Integration with a real payment gateway (Stripe/Razorpay).
* Live order tracking with Maps API.
* Push notifications for order status updates.
* User profile, wishlist, and discount coupons features.

---
*Developed as a demonstration of Android clean architecture and modern development practices.*
