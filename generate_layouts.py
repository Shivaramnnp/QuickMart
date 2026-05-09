import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip())

# Layouts
write_file('app/src/main/res/layout/activity_login.xml', """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="24dp">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="QuickMart"
        android:textSize="32sp"
        android:textStyle="bold"
        android:textColor="#0A84FF"
        android:layout_marginBottom="32dp"/>

    <EditText
        android:id="@+id/etPhone"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Mobile Number"
        android:inputType="phone"
        android:maxLength="10"
        android:padding="12dp"
        android:background="@android:drawable/edit_text"
        android:layout_marginBottom="16dp"/>

    <Button
        android:id="@+id/btnSendOtp"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Send OTP"
        android:backgroundTint="#0A84FF"
        android:textColor="#FFFFFF"
        android:layout_marginBottom="16dp"/>

    <EditText
        android:id="@+id/etOtp"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Enter OTP (1234)"
        android:inputType="number"
        android:maxLength="4"
        android:padding="12dp"
        android:background="@android:drawable/edit_text"
        android:layout_marginBottom="16dp"/>

    <Button
        android:id="@+id/btnVerifyOtp"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Verify &amp; Login"
        android:backgroundTint="#34C759"
        android:textColor="#FFFFFF"/>

</LinearLayout>
""")

write_file('app/src/main/res/layout/activity_home.xml', """
<?xml version="1.0" encoding="utf-8"?>
<androidx.coordinatorlayout.widget.CoordinatorLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#F5F5F5">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="vertical">

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="vertical"
            android:padding="16dp"
            android:background="#FFFFFF">
            
            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="QuickMart"
                android:textSize="24sp"
                android:textStyle="bold"
                android:textColor="#0A84FF"
                android:layout_marginBottom="16dp"/>

            <EditText
                android:id="@+id/etSearch"
                android:layout_width="match_parent"
                android:layout_height="48dp"
                android:hint="Search products..."
                android:background="#EFEFEF"
                android:padding="12dp"
                android:drawableStart="@android:drawable/ic_menu_search"
                android:drawablePadding="8dp"/>

            <HorizontalScrollView
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:scrollbars="none"
                android:layout_marginTop="12dp">

                <com.google.android.material.chip.ChipGroup
                    android:id="@+id/chipGroupCategories"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    app:singleSelection="true">

                    <com.google.android.material.chip.Chip
                        android:id="@+id/chipAll"
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="All"
                        style="@style/Widget.MaterialComponents.Chip.Choice"/>
                    <com.google.android.material.chip.Chip
                        android:id="@+id/chipFruits"
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="Fruits"
                        style="@style/Widget.MaterialComponents.Chip.Choice"/>
                    <com.google.android.material.chip.Chip
                        android:id="@+id/chipDairy"
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="Dairy"
                        style="@style/Widget.MaterialComponents.Chip.Choice"/>
                    <com.google.android.material.chip.Chip
                        android:id="@+id/chipSnacks"
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="Snacks"
                        style="@style/Widget.MaterialComponents.Chip.Choice"/>
                    <com.google.android.material.chip.Chip
                        android:id="@+id/chipBeverages"
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="Beverages"
                        style="@style/Widget.MaterialComponents.Chip.Choice"/>
                    <com.google.android.material.chip.Chip
                        android:id="@+id/chipBakery"
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="Bakery"
                        style="@style/Widget.MaterialComponents.Chip.Choice"/>

                </com.google.android.material.chip.ChipGroup>
            </HorizontalScrollView>
        </LinearLayout>

        <androidx.recyclerview.widget.RecyclerView
            android:id="@+id/rvProducts"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:padding="8dp"
            android:clipToPadding="false"/>

    </LinearLayout>

    <com.google.android.material.floatingactionbutton.FloatingActionButton
        android:id="@+id/fabCart"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="bottom|end"
        android:layout_margin="16dp"
        android:src="@android:drawable/ic_menu_myplaces"
        app:backgroundTint="#0A84FF"
        app:tint="#FFFFFF"/>
        
    <TextView
        android:id="@+id/tvCartCount"
        android:layout_width="24dp"
        android:layout_height="24dp"
        android:layout_gravity="bottom|end"
        android:layout_marginEnd="16dp"
        android:layout_marginBottom="46dp"
        android:background="#FF3B30"
        android:textColor="#FFFFFF"
        android:text="0"
        android:gravity="center"
        android:textStyle="bold"
        android:textSize="12sp"
        android:elevation="8dp"/>

</androidx.coordinatorlayout.widget.CoordinatorLayout>
""")

write_file('app/src/main/res/layout/item_product.xml', """
<?xml version="1.0" encoding="utf-8"?>
<androidx.cardview.widget.CardView xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:layout_margin="8dp"
    app:cardCornerRadius="12dp"
    app:cardElevation="4dp">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:padding="12dp">

        <ImageView
            android:id="@+id/ivProduct"
            android:layout_width="match_parent"
            android:layout_height="120dp"
            android:scaleType="centerCrop"
            android:background="#EEEEEE"/>

        <TextView
            android:id="@+id/tvProductName"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="Product Name"
            android:textStyle="bold"
            android:textSize="16sp"
            android:layout_marginTop="8dp"/>
            
        <TextView
            android:id="@+id/tvProductCategory"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="Category"
            android:textColor="#757575"
            android:textSize="12sp"/>

        <TextView
            android:id="@+id/tvProductPrice"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="₹100"
            android:textColor="#34C759"
            android:textStyle="bold"
            android:textSize="14sp"
            android:layout_marginTop="4dp"/>

        <Button
            android:id="@+id/btnAddToCart"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="Add to Cart"
            android:backgroundTint="#0A84FF"
            android:textColor="#FFFFFF"
            android:layout_marginTop="8dp"/>

    </LinearLayout>
</androidx.cardview.widget.CardView>
""")

write_file('app/src/main/res/layout/item_cart.xml', """
<?xml version="1.0" encoding="utf-8"?>
<androidx.cardview.widget.CardView xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:layout_marginHorizontal="16dp"
    android:layout_marginTop="8dp"
    app:cardCornerRadius="8dp"
    app:cardElevation="2dp">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:padding="12dp"
        android:gravity="center_vertical">

        <ImageView
            android:id="@+id/ivCartProduct"
            android:layout_width="60dp"
            android:layout_height="60dp"
            android:scaleType="centerCrop"
            android:background="#EEEEEE"/>

        <LinearLayout
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:orientation="vertical"
            android:layout_marginStart="12dp">

            <TextView
                android:id="@+id/tvCartProductName"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Product Name"
                android:textStyle="bold"
                android:textSize="16sp"/>

            <TextView
                android:id="@+id/tvCartProductPrice"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="₹100"
                android:textColor="#34C759"
                android:textStyle="bold"/>
        </LinearLayout>

        <LinearLayout
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:gravity="center_vertical"
            android:background="#EEEEEE"
            android:padding="4dp">

            <ImageButton
                android:id="@+id/btnDecrease"
                android:layout_width="32dp"
                android:layout_height="32dp"
                android:src="@android:drawable/ic_media_rew"
                android:background="?attr/selectableItemBackgroundBorderless"/>
                
            <TextView
                android:id="@+id/tvQuantity"
                android:layout_width="32dp"
                android:layout_height="wrap_content"
                android:text="1"
                android:gravity="center"
                android:textStyle="bold"/>

            <ImageButton
                android:id="@+id/btnIncrease"
                android:layout_width="32dp"
                android:layout_height="32dp"
                android:src="@android:drawable/ic_media_ff"
                android:background="?attr/selectableItemBackgroundBorderless"/>

        </LinearLayout>

    </LinearLayout>
</androidx.cardview.widget.CardView>
""")

print("Layouts written.")
