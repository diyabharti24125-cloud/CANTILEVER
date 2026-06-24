
import streamlit as st
import pandas as pd
from database import conn
from database import create_tables
from auth import register_user
from auth import login_user
import plotly.express as px

create_tables()


st.set_page_config(
    page_title="FinancePro",
    page_icon="💰",
    layout="wide"
)
if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

with open("styles.css") as f:

    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ==========================
# LOGIN PAGE
# ==========================

if not st.session_state.logged_in:

    st.markdown("""
    <h1 style='
    text-align:center;
    font-size:65px;
    font-weight:700;
    color:white;
    margin-bottom:0px;
    '>
    💰 FinancePro
    </h1>

    <p style='
    text-align:center;
    font-size:22px;
    color:#cbd5e1;
    '>
    Smart Personal Finance Management
    </p>
    """, unsafe_allow_html=True)

    login_tab, signup_tab = st.tabs(
        ["Login", "Sign Up"]
    )

    # LOGIN TAB
    with login_tab:

        left, center, right = st.columns([1,2,1])

        with center:

            st.markdown("""
            <div class="login-card">
            <h2 style='text-align:center;color:white'>
            Welcome Back
            </h2>

            <p style='text-align:center;color:#cbd5e1'>
            Login to continue
            </p>
            """, unsafe_allow_html=True)

            username = st.text_input(
                "Username",
                key="login_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            if st.button("Login"):

                user = login_user(
                    username,
                    password
                )

                if user:

                    st.session_state.logged_in = True
                    st.session_state.username = username

                    st.rerun()

                else:

                    st.error("Invalid Credentials")

    # SIGNUP TAB
    with signup_tab:

        left, center, right = st.columns([1,2,1])

        with center:

            st.markdown("""
            <div class="login-card">
            <h2 style='text-align:center;color:white'>
            Create Your Account
            </h2>

            <p style='text-align:center;color:#cbd5e1'>
            Start managing your finances today
            </p>
            """, unsafe_allow_html=True)

            new_user = st.text_input(
                "Username",
                key="signup_username"
            )

            email = st.text_input(
                "Email",
                key="signup_email"
            )

            new_pass = st.text_input(
                "Password",
                type="password",
                key="signup_password"
            )

            if st.button("Register"):

                success = register_user(
                    new_user,
                    email,
                    new_pass
                )

                if success:

                    st.success(
                        "Account Created Successfully!"
                    )

                else:

                    st.error(
                        "Username Already Exists"
                    )

# ==========================
# MAIN APPLICATION
# ==========================

else:
    df = pd.read_sql_query(
        """
        SELECT *
        FROM transactions
        WHERE username=?
        """,
        conn,
        params=(st.session_state.username,)
    )

    with st.sidebar:

        st.markdown(
            f"## 👤 {st.session_state.username}"
        )

        page = st.radio(
            "Navigation",
            [
              "Dashboard",
              "Transactions",
              "Analytics",
              "Reports",
              "Profile"  ]
     
        )

        if st.button("Logout"):

            st.session_state.logged_in = False
            st.rerun()
        st.markdown("---")

        st.caption("FinancePro v1.0")

        st.caption("Developed by Diya Bharti")    

    # Dashboard Page
    if page == "Dashboard":
     st.markdown(
     f"""
     <h1 style="color:white;font-size:48px;font-weight:700;">
        📊 Financial Dashboard
     </h1>

     <p style="color:#cbd5e1;font-size:22px;">
        Welcome back, {st.session_state.username}! 👋
     </p>
     """,
     unsafe_allow_html=True)

     df = pd.read_sql_query(
        """
        SELECT *
        FROM transactions
        WHERE username=?
        """,
        conn,
        params=(st.session_state.username,) )

     income = df[df["type"] == "Income"]["amount"].sum()

     expense = df[df["type"] == "Expense"]["amount"].sum()

     savings = income - expense
     col1, col2, col3, col4 = st.columns(4)

     with col1:
      st.markdown(f"""
     <div style="
     background:linear-gradient(135deg,#10b981,#059669);
     padding:25px;
     border-radius:20px;
     ">
        <h4>💰 Income</h4>
        <h2>₹{income:,.0f}</h2>
     </div>
     """, unsafe_allow_html=True)



     with col2:
      st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#ef4444,#dc2626);
    padding:25px;
    border-radius:20px;
    ">
        <h4>💸 Expense</h4>
        <h2>₹{expense:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

     with col3:
       st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#3b82f6,#8b5cf6);
    padding:25px;
    border-radius:20px;
    ">
        <h4>🏦 Savings</h4>
        <h2>₹{savings:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)
     budget = 50000
     budget_used = 0
     if budget > 0:
        budget_used = (expense / budget) * 100

     with col4:
       st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#f59e0b,#d97706);
    padding:25px;
    border-radius:20px;
    ">
        <h4>🎯 Budget Used</h4>
        <h2>{budget_used:.0f}%</h2>
    </div>
    """, unsafe_allow_html=True)
       
     st.markdown("## 💡 Smart Insights")
     if expense > income:
        st.error( "Expenses are higher than income. Consider reducing spending.")

     elif savings > income * 0.3:
        st.success("Excellent! You are saving more than 30% of your income.")

     else:
        st.warning( "Try increasing your monthly savings.")

     st.markdown("## 📅 Monthly Summary")
     col1, col2 = st.columns(2)

     with col1:

       st.info(f"Total Income: ₹{income:,.0f}")

     with col2:

       st.info( f"Total Expenses: ₹{expense:,.0f}")
       

     st.markdown("### 💪 Financial Health Score")
     score = 0

     if income > 0:
      score = min(
        int((savings / income) * 100),
        100
     )
     st.progress(score / 100)
     st.success(
     f"Financial Score: {score}/100")

     st.markdown("### 📜 Recent Transactions")
     st.dataframe(
     df.tail(5),
     use_container_width=True)

    # Transactions Page

    elif page == "Transactions":

     st.title("💳 Transactions")

     col1, col2 = st.columns(2)

     with col1:

        transaction_type = st.selectbox(
            "Type",
            ["Income", "Expense"]
        )

        category = st.selectbox(
            "Category",
            [
                "Salary",
                "Food",
                "Travel",
                "Shopping",
                "Bills",
                "Health",
                "Other"
            ]
        )

     with col2:

        amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=100.0
        )

        date = st.date_input(
            "Date"
        )

     if st.button("Save Transaction"):

        conn.execute(
            """
            INSERT INTO transactions
            (
                username,
                type,
                category,
                amount,
                date
            )
            VALUES (?,?,?,?,?)
            """,
            (
                st.session_state.username,
                transaction_type,
                category,
                amount,
                str(date)
            )
        )

        conn.commit()

        st.success(
            "Transaction Added Successfully!"
        )

     st.divider()

     df = pd.read_sql_query(
        """
        SELECT *
        FROM transactions
        WHERE username=?
        ORDER BY id DESC
        """,
        conn,
        params=(st.session_state.username,))

     st.subheader("Transaction History")

     st.dataframe(
        df,use_container_width=True)

     st.subheader("Delete Transaction")
     transaction_id = st.number_input( "Transaction ID",min_value=1)
     if st.button("Delete"):

       conn.execute(
        """
        DELETE FROM transactions
        WHERE id=?
        """,
        (transaction_id,)
        )

       conn.commit()

       st.success(
        "Transaction Deleted")
        

    # Analytics Page

    elif page == "Analytics":

        st.title("📈 Analytics")
        expense_df = df[ df["type"] == "Expense"]
        # Load user data
        df = pd.read_sql_query("""

        SELECT * FROM transactions
        WHERE username=? 
        """,
        conn,
        params=(st.session_state.username,))

       # Calculate totals

        income = df[df["type"] == "Income"]["amount"].sum()

        expense = df[df["type"] == "Expense"]["amount"].sum()

        savings = income - expense

        expense_df = df[df["type"] == "Expense"]
        if not expense_df.empty:

          category_expense = (expense_df.groupby("category")["amount"].sum().reset_index())

          fig = px.pie(category_expense,names="category",values="amount",title="Expense Breakdown")

          st.plotly_chart(fig,use_container_width=True)

          fig2 = px.bar(
          category_expense,
           x="category",
           y="amount",
           title="Expenses by Category")

          st.plotly_chart(fig2,use_container_width=True)

          comparison_df = pd.DataFrame({
            "Type":["Income","Expense"],
             "Amount":[income,expense]})
          
          fig3 = px.bar(
             comparison_df,
             x="Type",
             y="Amount",
             title="Income vs Expense")

          st.plotly_chart( fig3,use_container_width=True)

          st.markdown("## 🔮 Future Savings Prediction")
          predicted_savings = savings * 12
          st.success(f"Estimated Annual Savings: ₹{predicted_savings:,.0f}")

    # Reports Page

    elif page == "Reports":
        st.title("📄 Reports")
        csv = df.to_csv(index=False)
        st.download_button(
          "Download CSV Report",
           csv,
          "finance_report.csv",
          "text/csv")
        
    elif page == "Profile":
       st.title("👤 Profile")

       st.write(f"Username: {st.session_state.username}")