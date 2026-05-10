import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip())

# Update item_product.xml to support quantity controls
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

        <FrameLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="8dp">

            <Button
                android:id="@+id/btnAddToCart"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:text="Add to Cart"
                android:backgroundTint="#0A84FF"
                android:textColor="#FFFFFF"/>

            <LinearLayout
                android:id="@+id/llQuantityControl"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:orientation="horizontal"
                android:gravity="center"
                android:visibility="gone"
                android:background="#EEEEEE"
                android:padding="4dp"
                android:layout_gravity="center">

                <ImageButton
                    android:id="@+id/btnDecrease"
                    android:layout_width="40dp"
                    android:layout_height="40dp"
                    android:src="@android:drawable/ic_media_rew"
                    android:background="?attr/selectableItemBackgroundBorderless"/>
                    
                <TextView
                    android:id="@+id/tvQuantity"
                    android:layout_width="0dp"
                    android:layout_weight="1"
                    android:layout_height="wrap_content"
                    android:text="1"
                    android:gravity="center"
                    android:textSize="16sp"
                    android:textStyle="bold"/>

                <ImageButton
                    android:id="@+id/btnIncrease"
                    android:layout_width="40dp"
                    android:layout_height="40dp"
                    android:src="@android:drawable/ic_media_ff"
                    android:background="?attr/selectableItemBackgroundBorderless"/>

            </LinearLayout>
        </FrameLayout>

    </LinearLayout>
</androidx.cardview.widget.CardView>
""")

# Setup Night Theme
write_file('app/src/main/res/values-night/themes.xml', """
<resources xmlns:tools="http://schemas.android.com/tools">
    <style name="Theme.QuickMart" parent="Theme.MaterialComponents.DayNight.NoActionBar">
        <item name="colorPrimary">#0A84FF</item>
        <item name="colorPrimaryVariant">#005BB5</item>
        <item name="colorOnPrimary">#FFFFFF</item>
        <item name="colorSecondary">#34C759</item>
        <item name="colorSecondaryVariant">#28A745</item>
        <item name="colorOnSecondary">#000000</item>
        <item name="colorError">#CF6679</item>
        <item name="colorOnError">#000000</item>
        <item name="colorSurface">#1E1E1E</item>
        <item name="colorOnSurface">#FFFFFF</item>
        <item name="android:colorBackground">#121212</item>
        <item name="colorOnBackground">#FFFFFF</item>
    </style>
</resources>
""")

# Since we want animateLayoutChanges, we can inject them to activity_home and activity_cart
def add_animate_layout(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Simple search & replace to add the property
    content = content.replace('android:layout_width="match_parent"\\n    android:layout_height="match_parent"',
                              'android:layout_width="match_parent"\\n    android:layout_height="match_parent"\\n    android:animateLayoutChanges="true"')
    with open(filepath, 'w') as f:
        f.write(content)

add_animate_layout('app/src/main/res/layout/activity_home.xml')
add_animate_layout('app/src/main/res/layout/activity_cart.xml')

print("Done generating XML fixes!")
