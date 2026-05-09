import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip())

write_file('app/src/main/res/layout/activity_cart.xml', """
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#F5F5F5">

    <TextView
        android:id="@+id/tvCartTitle"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="My Cart"
        android:textSize="20sp"
        android:textStyle="bold"
        android:padding="16dp"
        android:background="#FFFFFF"
        android:elevation="4dp"/>

    <LinearLayout
        android:id="@+id/llEmptyCart"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:layout_below="@id/tvCartTitle"
        android:orientation="vertical"
        android:gravity="center"
        android:visibility="gone">

        <ImageView
            android:layout_width="120dp"
            android:layout_height="120dp"
            android:src="@android:drawable/ic_menu_myplaces"
            app:tint="#CCCCCC"/>

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Your cart is empty!"
            android:textSize="18sp"
            android:textColor="#757575"
            android:layout_marginTop="16dp"/>

        <Button
            android:id="@+id/btnStartShopping"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Start Shopping"
            android:layout_marginTop="16dp"
            android:backgroundTint="#0A84FF"
            android:textColor="#FFFFFF"/>
    </LinearLayout>

    <androidx.recyclerview.widget.RecyclerView
        android:id="@+id/rvCartItems"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:layout_below="@id/tvCartTitle"
        android:layout_above="@id/cvBillSummary"
        android:clipToPadding="false"
        android:paddingBottom="16dp"/>

    <androidx.cardview.widget.CardView
        android:id="@+id/cvBillSummary"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_above="@id/btnCheckout"
        app:cardElevation="8dp"
        app:cardCornerRadius="0dp">

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="vertical"
            android:padding="16dp">

            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Bill Summary"
                android:textStyle="bold"
                android:textSize="16sp"
                android:layout_marginBottom="12dp"/>

            <LinearLayout
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:orientation="horizontal"
                android:layout_marginBottom="8dp">
                <TextView
                    android:layout_width="0dp"
                    android:layout_height="wrap_content"
                    android:layout_weight="1"
                    android:text="Item Total"/>
                <TextView
                    android:id="@+id/tvItemTotal"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="₹0"/>
            </LinearLayout>

            <LinearLayout
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:orientation="horizontal"
                android:layout_marginBottom="12dp">
                <TextView
                    android:layout_width="0dp"
                    android:layout_height="wrap_content"
                    android:layout_weight="1"
                    android:text="Delivery Charge"/>
                <TextView
                    android:id="@+id/tvDeliveryCharge"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="₹30"/>
            </LinearLayout>

            <View
                android:layout_width="match_parent"
                android:layout_height="1dp"
                android:background="#E0E0E0"
                android:layout_marginBottom="12dp"/>

            <LinearLayout
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:orientation="horizontal">
                <TextView
                    android:layout_width="0dp"
                    android:layout_height="wrap_content"
                    android:layout_weight="1"
                    android:text="Grand Total"
                    android:textStyle="bold"
                    android:textSize="18sp"/>
                <TextView
                    android:id="@+id/tvGrandTotal"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="₹0"
                    android:textStyle="bold"
                    android:textSize="18sp"
                    android:textColor="#34C759"/>
            </LinearLayout>
        </LinearLayout>
    </androidx.cardview.widget.CardView>

    <Button
        android:id="@+id/btnCheckout"
        android:layout_width="match_parent"
        android:layout_height="56dp"
        android:layout_alignParentBottom="true"
        android:text="Proceed to Checkout"
        android:backgroundTint="#0A84FF"
        android:textColor="#FFFFFF"
        android:textSize="16sp"
        android:textStyle="bold"
        app:cornerRadius="0dp"/>

</RelativeLayout>
""")

write_file('app/src/main/res/layout/activity_checkout.xml', """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:background="#F5F5F5">

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Checkout"
        android:textSize="20sp"
        android:textStyle="bold"
        android:padding="16dp"
        android:background="#FFFFFF"
        android:elevation="4dp"/>

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:padding="16dp"
        android:background="#FFFFFF"
        android:layout_marginTop="16dp">

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Delivery Address"
            android:textStyle="bold"
            android:textSize="16sp"
            android:layout_marginBottom="12dp"/>

        <EditText
            android:id="@+id/etAddress"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:minLines="3"
            android:gravity="top|start"
            android:hint="Enter complete delivery address"
            android:background="@android:drawable/edit_text"
            android:padding="12dp"/>
    </LinearLayout>

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:padding="16dp"
        android:background="#FFFFFF"
        android:layout_marginTop="16dp">

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Payment Method"
            android:textStyle="bold"
            android:textSize="16sp"
            android:layout_marginBottom="12dp"/>

        <RadioGroup
            android:id="@+id/rgPayment"
            android:layout_width="match_parent"
            android:layout_height="wrap_content">

            <RadioButton
                android:id="@+id/rbCod"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:text="Cash on Delivery (COD)"
                android:padding="8dp"/>

            <RadioButton
                android:id="@+id/rbOnline"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:text="Online Payment (UPI / Cards)"
                android:padding="8dp"/>

        </RadioGroup>
    </LinearLayout>

    <View
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1"/>

    <Button
        android:id="@+id/btnPlaceOrder"
        android:layout_width="match_parent"
        android:layout_height="56dp"
        android:text="Place Order"
        android:backgroundTint="#34C759"
        android:textColor="#FFFFFF"
        android:textSize="16sp"
        android:textStyle="bold"
        android:layout_margin="16dp"/>

</LinearLayout>
""")

write_file('app/src/main/res/layout/activity_order_success.xml', """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="24dp"
    android:background="#FFFFFF">

    <ImageView
        android:layout_width="120dp"
        android:layout_height="120dp"
        android:src="@android:drawable/ic_dialog_info"
        app:tint="#34C759"
        android:layout_marginBottom="24dp"/>

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Order Placed Successfully!"
        android:textSize="24sp"
        android:textStyle="bold"
        android:textColor="#34C759"
        android:gravity="center"
        android:layout_marginBottom="32dp"/>

    <androidx.cardview.widget.CardView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        app:cardCornerRadius="12dp"
        app:cardElevation="4dp"
        android:layout_marginBottom="32dp"
        app:cardBackgroundColor="#F5F5F5">

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="vertical"
            android:padding="16dp"
            android:gravity="center">

            <TextView
                android:id="@+id/tvOrderId"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Order ID: QM1024"
                android:textStyle="bold"
                android:textSize="16sp"
                android:layout_marginBottom="8dp"/>

            <TextView
                android:id="@+id/tvDeliveryTime"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Estimated delivery: 15–20 mins"
                android:textColor="#757575"
                android:textSize="14sp"/>
        </LinearLayout>
    </androidx.cardview.widget.CardView>

    <Button
        android:id="@+id/btnContinueShopping"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Continue Shopping"
        android:backgroundTint="#0A84FF"
        android:textColor="#FFFFFF"/>

</LinearLayout>
""")

print("Layouts 2 written.")
