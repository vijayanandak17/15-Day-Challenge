import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import base64
from io import BytesIO

# Configure the page
st.set_page_config(
    page_title="Restaurant Order & Billing",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #ff6b6b, #ffa500);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    .menu-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        color: white;
    }
    
    .menu-item {
        background: rgba(255,255,255,0.1);
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        border-left: 4px solid #ffa500;
    }
    
    .price-tag {
        background: #ff6b6b;
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-weight: bold;
    }
    
    .order-summary {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    
    .bill-total {
        background: #ff6b6b;
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5em;
        font-weight: bold;
    }
    
    .stSelectbox > div > div {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# Menu data structure
MENU_DATA = {
    "🥗 Appetizers & Salads": {
        "Caesar Salad": 8.50,
        "Greek Salad": 9.25,
        "Garlic Bread": 4.50,
        "Mozzarella Sticks": 6.75,
        "Chicken Wings": 11.50,
        "Onion Rings": 5.25,
        "Bruschetta": 7.50
    },
    "🍝 Pasta & Italian": {
        "Spaghetti Carbonara": 14.50,
        "Penne Arrabbiata": 12.75,
        "Fettuccine Alfredo": 13.25,
        "Lasagna Bolognese": 16.50,
        "Ravioli Spinach": 15.25,
        "Gnocchi Pesto": 14.75,
        "Linguine Seafood": 18.50
    },
    "🍔 Burgers & Sandwiches": {
        "Classic Beef Burger": 12.50,
        "Chicken Avocado Burger": 13.75,
        "Veggie Burger": 11.25,
        "BBQ Bacon Burger": 14.50,
        "Fish Sandwich": 13.25,
        "Grilled Cheese": 8.50,
        "Club Sandwich": 12.75
    },
    "🥩 Main Courses": {
        "Grilled Salmon": 22.50,
        "Ribeye Steak": 28.75,
        "Chicken Parmesan": 19.50,
        "Pork Tenderloin": 21.25,
        "Lamb Chops": 26.50,
        "Fish & Chips": 16.75,
        "Vegetarian Platter": 15.50
    },
    "🍕 Pizza": {
        "Margherita Pizza": 14.50,
        "Pepperoni Pizza": 16.25,
        "Hawaiian Pizza": 17.50,
        "Meat Lovers Pizza": 19.75,
        "Veggie Supreme": 18.25,
        "BBQ Chicken Pizza": 18.50,
        "Four Cheese Pizza": 17.25
    },
    "🍰 Desserts": {
        "Chocolate Cake": 6.50,
        "Tiramisu": 7.25,
        "Cheesecake": 6.75,
        "Ice Cream Sundae": 5.50,
        "Apple Pie": 6.25,
        "Crème Brûlée": 7.75,
        "Gelato (3 scoops)": 5.75
    },
    "☕ Beverages": {
        "Fresh Orange Juice": 4.50,
        "Coffee": 3.25,
        "Cappuccino": 4.75,
        "Soft Drinks": 2.95,
        "Iced Tea": 3.50,
        "Hot Chocolate": 4.25,
        "Mineral Water": 2.50
    }
}

def add_to_cart(item_name, price, quantity):
    """Add item to cart"""
    if quantity > 0:
        if item_name in st.session_state.cart:
            st.session_state.cart[item_name]['quantity'] += quantity
        else:
            st.session_state.cart[item_name] = {'price': price, 'quantity': quantity}

def remove_from_cart(item_name):
    """Remove item from cart"""
    if item_name in st.session_state.cart:
        del st.session_state.cart[item_name]

def calculate_totals():
    """Calculate cart totals"""
    subtotal = sum(item['price'] * item['quantity'] for item in st.session_state.cart.values())
    tax_rate = 0.08  # 8% tax
    tax = subtotal * tax_rate
    total = subtotal + tax
    return subtotal, tax, total

def generate_pdf_invoice():
    """Generate PDF invoice"""
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 15)
            self.cell(0, 10, 'Restaurant Invoice', 0, 1, 'C')
            self.ln(10)
        
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    pdf = PDF()
    pdf.add_page()
    
    # Invoice header
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1)
    pdf.cell(0, 10, 'Phone: 088/445 45 451', 0, 1)
    pdf.ln(10)
    
    # Table header
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(80, 10, 'Item', 1, 0, 'C')
    pdf.cell(30, 10, 'Quantity', 1, 0, 'C')
    pdf.cell(30, 10, 'Price', 1, 0, 'C')
    pdf.cell(30, 10, 'Total', 1, 1, 'C')
    
    # Table content
    pdf.set_font('Arial', '', 9)
    for item_name, details in st.session_state.cart.items():
        pdf.cell(80, 8, item_name[:25], 1, 0)
        pdf.cell(30, 8, str(details['quantity']), 1, 0, 'C')
        pdf.cell(30, 8, f'${details["price"]:.2f}', 1, 0, 'C')
        pdf.cell(30, 8, f'${details["price"] * details["quantity"]:.2f}', 1, 1, 'C')
    
    # Totals
    subtotal, tax, total = calculate_totals()
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(140, 8, 'Subtotal:', 0, 0, 'R')
    pdf.cell(30, 8, f'${subtotal:.2f}', 1, 1, 'C')
    pdf.cell(140, 8, 'Tax (8%):', 0, 0, 'R')
    pdf.cell(30, 8, f'${tax:.2f}', 1, 1, 'C')
    pdf.cell(140, 8, 'Total:', 0, 0, 'R')
    pdf.cell(30, 8, f'${total:.2f}', 1, 1, 'C')
    
    return pdf.output(dest='S').encode('latin-1')

# Main App Layout
st.markdown('<div class="main-header">🍽️ RESTAURANT MENU & ORDERING</div>', unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📋 Menu Items")
    
    # Display menu sections
    for section_name, items in MENU_DATA.items():
        with st.expander(f"{section_name}", expanded=False):
            st.markdown(f'<div class="menu-section">', unsafe_allow_html=True)
            
            for item_name, price in items.items():
                col_item, col_price, col_qty, col_btn = st.columns([3, 1, 1, 1])
                
                with col_item:
                    st.markdown(f"**{item_name}**")
                
                with col_price:
                    st.markdown(f'<span class="price-tag">${price:.2f}</span>', unsafe_allow_html=True)
                
                with col_qty:
                    quantity = st.number_input(
                        "Qty", 
                        min_value=0, 
                        max_value=20, 
                        value=0, 
                        step=1, 
                        key=f"qty_{item_name}",
                        label_visibility="collapsed"
                    )
                
                with col_btn:
                    if st.button("Add", key=f"add_{item_name}", type="primary"):
                        if quantity > 0:
                            add_to_cart(item_name, price, quantity)
                            st.success(f"Added {quantity}x {item_name}")
                            st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### 🛒 Order Summary")
    
    if st.session_state.cart:
        st.markdown('<div class="order-summary">', unsafe_allow_html=True)
        
        # Display cart items
        for item_name, details in st.session_state.cart.items():
            col_name, col_details, col_remove = st.columns([2, 1, 1])
            
            with col_name:
                st.write(f"**{item_name[:20]}**")
            
            with col_details:
                st.write(f"{details['quantity']}x ${details['price']:.2f}")
                st.write(f"= ${details['price'] * details['quantity']:.2f}")
            
            with col_remove:
                if st.button("❌", key=f"remove_{item_name}"):
                    remove_from_cart(item_name)
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Calculate and display totals
        subtotal, tax, total = calculate_totals()
        
        st.markdown("---")
        
        # Bill summary
        st.markdown('<div class="bill-total">', unsafe_allow_html=True)
        st.write(f"**Subtotal: ${subtotal:.2f}**")
        st.write(f"**Tax (8%): ${tax:.2f}**")
        st.write(f"**Total: ${total:.2f}**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Action buttons
        st.markdown("---")
        
        col_clear, col_pdf = st.columns(2)
        
        with col_clear:
            if st.button("🗑️ Clear Cart", type="secondary", use_container_width=True):
                st.session_state.cart = {}
                st.rerun()
        
        with col_pdf:
            if st.button("📄 Download Invoice", type="primary", use_container_width=True):
                try:
                    pdf_data = generate_pdf_invoice()
                    b64 = base64.b64encode(pdf_data).decode()
                    href = f'<a href="data:application/octet-stream;base64,{b64}" download="restaurant_invoice_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf">Download Invoice PDF</a>'
                    st.markdown(href, unsafe_allow_html=True)
                    st.success("Invoice generated successfully!")
                except Exception as e:
                    st.error("PDF generation requires fpdf2 library. Install it with: pip install fpdf2")
    
    else:
        st.info("🛒 Your cart is empty. Add some items from the menu!")
        st.markdown("---")
        st.markdown("📞 **Contact Us**")
        st.write("📱 088/445 45 451")
        st.write("🕒 Open daily 11:00 AM - 11:00 PM")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>🍽️ Thank you for dining with us! 🍽️</p>
        <p>📞 For reservations call: 088/445 45 451</p>
    </div>
    """, 
    unsafe_allow_html=True
)