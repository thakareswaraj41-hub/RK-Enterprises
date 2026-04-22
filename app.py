from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from bson import ObjectId 
import os
from flask import render_template, request, redirect, url_for, session, flash
from bson.objectid import ObjectId # Ensure this import is at the top of app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from datetime import datetime
from twilio.rest import Client
import random
from flask import Flask, request, jsonify, session, url_for, render_template
import smtplib
import random
from datetime import datetime
from email.mime.text import MIMEText
from flask import Flask, request, jsonify, session, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
import random
from email.mime.text import MIMEText
from flask import Flask, request, jsonify, session
import smtplib
import random
import smtplib
import random
from email.mime.text import MIMEText
from flask import Flask, request, jsonify, session, redirect, url_for, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from email.mime.text import MIMEText
from flask import Flask, request, jsonify, session, redirect, url_for, render_template, flash
from werkzeug.security import check_password_hash
import certifi
# ... keep your existing mongo imports like users_col here ...


app = Flask(__name__)
app.secret_key = "rk_enterprises_secret_key"

# MongoDB Connection
try:
    MONGO_URI = os.environ.get("MONGO_URI")
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    db = client["RK_Enterprises_DB"]
    users_col = db["users"]
    projects_col = db["projects"]
    boq_col = db["boq"]
    bom_col = db["bom"]
    bills_col = db["ra_bills"]

    client.server_info()
    print("MongoDB Atlas Connected ✅")

except Exception as e:
    print("MongoDB Error:", e)

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# --- AUTHENTICATION ROUTES ---



# 1. ALWAYS DEFINE THE APP FIRST
app = Flask(__name__)
app.secret_key = "rk_erp_secure_key_2026"

# 2. DEFINE YOUR GLOBAL CONFIGURATION
SENDER_EMAIL = "thakareswaraj41@gmail.com" 
SENDER_PASSWORD = "rxkzwhkwfzfdmzwh" # NO SPACES HERE

# 3. NOW DEFINE YOUR ROUTES
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_col.find_one({"username": username})
        
        if user and check_password_hash(user['password'], password):
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid Username or Password")
            
    return render_template('login.html')


app = Flask(__name__)
app.secret_key = "rk_erp_secure_key_2026"

# Configuration - Ensure SENDER_PASSWORD has no spaces
SENDER_EMAIL = "thakareswaraj41@gmail.com" 
SENDER_PASSWORD = "rxkzwhkwfzfdmzwh" 

# --- ROUTES ---

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Replace with your actual MongoDB collection check
        user = users_col.find_one({"username": username})
        if user and check_password_hash(user['password'], password):
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid Username or Password")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if user exists
        if users_col.find_one({"username": username}):
            return jsonify({"success": False, "message": "User already exists"}), 400
        
        # Save User to MongoDB
        hashed_pw = generate_password_hash(password)
        users_col.insert_one({
            "username": username,
            "password": hashed_pw,
            "email": "thakareswaraj41@gmail.com",
            "created_at": datetime.now()
        })
        return jsonify({"success": True, "redirect": url_for('login')})
    
    return render_template('signup.html')

@app.route('/send_otp', methods=['POST'])
def send_otp():
    receiver_email = "thakareswaraj41@gmail.com" 
    otp = str(random.randint(100000, 999999))
    session['signup_otp'] = otp 

    msg = MIMEText(f"Your RK ERP verification code is: {otp}")
    msg['Subject'] = 'RK ERP Security Code'
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        return jsonify({"success": True, "msg": "OTP sent to your Gmail!"})
    except Exception as e:
        return jsonify({"success": False, "msg": f"Error: {str(e)}"})

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    user_otp = data.get('otp')
    stored_otp = session.get('signup_otp')
    if stored_otp and str(user_otp) == str(stored_otp):
        return jsonify({"success": True})
    return jsonify({"success": False, "msg": "Invalid OTP"})


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']
        hashed_pw = generate_password_hash(new_password)
        result = users_col.update_one({"username": username}, {"$set": {"password": hashed_pw}})
        if result.matched_count > 0:
            flash("Password updated successfully!")
            return redirect(url_for('login'))
        else:
            flash("User not found.")
    return render_template('forgot.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# --- MAIN APP ROUTES ---

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/project', methods=['GET', 'POST'])
def project():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        project_data = {
            "project_id": request.form['project_id'],
            "client_name": request.form['client_name'],
            "panel_type": request.form['panel_type'],
            "deadline": request.form['deadline'],
            "status": "In Progress"
        }
        projects_col.insert_one(project_data)
        flash("Project saved successfully!")
        return redirect(url_for('project'))

    all_projects = list(projects_col.find())
    return render_template('project.html', projects=all_projects)

@app.route('/workorder', methods=['GET', 'POST'])
def workorder():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    last_p = None

    if request.method == 'POST':
        p_ref = request.form.get('project_ref')
        
        boq_data = {
            "project_ref": p_ref,
            "workorder_no": request.form.get('workorder_no'),
            "subject": request.form.get('subject'),
            "description": request.form.get('description')
        }
        boq_col.insert_one(boq_data)
        flash("Work order item added successfully!")
        
        # Set the memory variable
        last_p = p_ref

    all_projects = list(projects_col.find())
    all_boqs = list(boq_col.find())
    
    return render_template('workorder.html', 
                           projects=all_projects, 
                           boqs=all_boqs, 
                           last_p=last_p)
@app.route('/bom', methods=['GET', 'POST'])
def bom():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Initialize these as None for GET requests
    last_p = None
    last_w = None

    if request.method == 'POST':
        # 1. Capture Form Data
        p_id = request.form.get('project_ref')
        w_id = request.form.get('workorder_no')
        
        bom_data = {
            "project_ref": p_id,
            "workorder_no": w_id,
            "material_name": request.form.get('material_name'), # Added material_name
            "description": request.form.get('description'),
            "qty": request.form.get('qty'),
            "unit": request.form.get('unit'),
            "tender_rate": request.form.get('tender_rate'),
            "amount": request.form.get('amount')
        }
        
        # 2. Save to MongoDB
        bom_col.insert_one(bom_data)
        flash("BOM Entry Saved!")
        
        # 3. Set variables to pass back to the template
        last_p = p_id
        last_w = w_id

    # Common data needed for both GET and POST
    all_projects = list(projects_col.find())
    all_workorders = list(boq_col.find()) 
    all_boms = list(bom_col.find())
    
    return render_template('bom.html', 
                           projects=all_projects, 
                           workorders=all_workorders, 
                           boms=all_boms,
                           last_p=last_p, 
                           last_w=last_w)

@app.route('/billing', methods=['GET', 'POST'])
def billing():
    if 'user' not in session:
        return redirect(url_for('login'))

    selected_p = request.args.get('project_ref')
    selected_w = request.args.get('workorder_no')
    edit_mode_id = request.args.get('edit_bill_id')

    # --- 1. POST: Save or Update Logic ---
    if request.method == 'POST':
        p_ref = request.form.get('project_ref')
        w_ref = request.form.get('workorder_no')
        b_num = int(request.form.get('bill_no', 1))
        target_id = request.form.get('edit_target_id')

        m_ids = request.form.getlist('bom_id')
        p_qtys = request.form.getlist('present_qty')

        # Renamed key to bill_items to avoid the Jinja2 dict.items() conflict
        items_data = [
            {
                "bom_id": mid, 
                "qty": float(p_qty) if p_qty and p_qty.strip() else 0.0
            } for mid, p_qty in zip(m_ids, p_qtys)
        ]

        if target_id:
            # UPDATE existing bill
            bills_col.update_one(
                {"_id": ObjectId(target_id)}, 
                {"$set": {"bill_items": items_data}}
            )
            flash(f"RA Bill No {b_num} updated successfully!")
        else:
            # SAVE new bill
            bills_col.insert_one({
                "project_ref": p_ref, 
                "workorder_no": w_ref, 
                "bill_no": b_num, 
                "bill_items": items_data
            })
            flash(f"RA Bill No {b_num} saved successfully!")

        return redirect(url_for('billing', project_ref=p_ref, workorder_no=w_ref))

    # --- 2. GET: Load Data Logic ---
    bom_items = []
    past_bills = []
    edit_data_map = {}
    bill_no = 1

    if selected_p and selected_w:
        # Load bill history
        past_bills = list(bills_col.find({
            "project_ref": selected_p, 
            "workorder_no": selected_w
        }).sort("bill_no", -1))

        if edit_mode_id:
            editing_bill = bills_col.find_one({"_id": ObjectId(edit_mode_id)})
            if editing_bill:
                bill_no = editing_bill['bill_no']
                # Support both naming conventions during transition
                source = editing_bill.get('bill_items', editing_bill.get('items', []))
                edit_data_map = {item['bom_id']: item['qty'] for item in source}
        else:
            # Auto-increment bill number for new drafts
            last = bills_col.find_one(
                {"project_ref": selected_p, "workorder_no": selected_w}, 
                sort=[("bill_no", -1)]
            )
            bill_no = (last['bill_no'] + 1) if last else 1

        # Fetch BOM and calculate totals
        bom_items = list(bom_col.find({"project_ref": selected_p, "workorder_no": selected_w}))
        
        for item in bom_items:
            item_str_id = str(item['_id'])
            
            # Aggregation pipeline handles both legacy 'items' and new 'bill_items'
            pipeline = [
                {"$match": {
                    "project_ref": selected_p, 
                    "workorder_no": selected_w, 
                    "bill_no": {"$lt": bill_no}
                }},
                {"$project": {
                    "bill_data": {"$ifNull": ["$bill_items", "$items"]}
                }},
                {"$unwind": "$bill_data"},
                {"$match": {"bill_data.bom_id": item_str_id}},
                {"$group": {"_id": None, "total": {"$sum": "$bill_data.qty"}}}
            ]
            
            res = list(bills_col.aggregate(pipeline))
            prev_qty = res[0]['total'] if res else 0
            rate = float(item.get('tender_rate', 0) or 0)
            
            item.update({
                'prev_qty': prev_qty, 
                'prev_amt': prev_qty * rate, 
                'edit_qty': edit_data_map.get(item_str_id, 0) if edit_mode_id else ""
            })

    return render_template('billing.html', 
                           projects=list(projects_col.find()), 
                           workorders=list(boq_col.find({"project_ref": selected_p})) if selected_p else [], 
                           bom_items=bom_items, 
                           past_bills=past_bills, 
                           selected_p=selected_p or "", 
                           selected_w=selected_w or "", 
                           bill_no=bill_no, 
                           edit_target_id=edit_mode_id)
# 1. INVENTORY: Define Materials here


@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if request.method == 'POST':
        mat_id = request.form.get('material_id')
        data = {
            "material_name": request.form.get('material_name').strip(),
            "description": request.form.get('description'),
            "unit": request.form.get('unit')
        }
        
        if mat_id:
            db.materials.update_one({"_id": ObjectId(mat_id)}, {"$set": data})
        else:
            db.materials.insert_one(data)
            
        return redirect(url_for('inventory'))

    # GET Logic
    edit_id = request.args.get('edit_id')
    edit_material = db.materials.find_one({"_id": ObjectId(edit_id)}) if edit_id else None
    
    materials = list(db.materials.find())
    inventory_list = []
    
    for mat in materials:
        name = mat['material_name']
        
        # 1. Sum all PURCHASES (Inward)
        purchases = list(db.purchases.find({"material_name": name}))
        total_purchased = sum(p.get('qty', 0) for p in purchases)
        
        # 2. Sum all DISPATCHES (Outward)
        dispatches = list(db.dispatches.find({"material_name": name}))
        total_dispatched = sum(d.get('qty', 0) for d in dispatches)
        
        # 3. Final Stock = In - Out
        mat['total_qty'] = total_purchased - total_dispatched
        inventory_list.append(mat)

    return render_template('inventory.html', 
                           inventory=inventory_list, 
                           edit_material=edit_material)
    


@app.route('/quotation', methods=['GET', 'POST'])
def quotation():
    if request.method == 'POST':
        # Collect Customer Info
        customer_data = {
            "customer_name": request.form.get('customer_name'),
            "address": request.form.get('address'),
            "gstin": request.form.get('gstin'),
            "date": request.form.get('date') or datetime.now().strftime("%d-%m-%Y"),
            "items": []
        }

        # Match these keys exactly with the 'name' attributes in HTML
        materials = request.form.getlist('item_name[]')
        descriptions = request.form.getlist('item_desc[]')
        qtys = request.form.getlist('item_qty[]')
        units = request.form.getlist('item_unit[]')
        rates = request.form.getlist('item_rate[]')

        subtotal = 0
        for i in range(len(materials)):
            try:
                qty = float(qtys[i]) if qtys[i] else 0.0
                rate = float(rates[i]) if rates[i] else 0.0
                amount = qty * rate
                subtotal += amount
                
                customer_data["items"].append({
                    "material": materials[i],
                    "description": descriptions[i],
                    "qty": qty,
                    "unit": units[i],
                    "rate": rate,
                    "amount": amount
                })
            except (IndexError, ValueError):
                continue

        customer_data["subtotal"] = subtotal
        customer_data["gst_amount"] = subtotal * 0.18
        customer_data["grand_total"] = subtotal + customer_data["gst_amount"]

        db.quotations.insert_one(customer_data)
        return redirect(url_for('quotation_history'))

    current_date = datetime.now().strftime("%d-%m-%Y")
    return render_template('quotation.html', current_date=current_date)


@app.route('/delete_inventory/<mat_id>')
def delete_inventory(mat_id):
    db.materials.delete_one({"_id": ObjectId(mat_id)})
    return redirect(url_for('inventory'))

# 2. PURCHASE: Select from existing Materials
@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        p_id = request.form.get('purchase_id')
        
        # Ensure all fields are captured
        data = {
            "material_name": request.form.get('material_name'),
            "qty": float(request.form.get('qty') or 0),
            "rate": float(request.form.get('rate') or 0),
            "supplier": request.form.get('supplier'),
            "date": request.form.get('date'),
            "description": request.form.get('description')
        }
        
        if p_id:
            db.purchases.update_one({"_id": ObjectId(p_id)}, {"$set": data})
        else:
            db.purchases.insert_one(data)
        return redirect(url_for('purchase'))

    # GET logic
    edit_id = request.args.get('edit_id')
    edit_val = db.purchases.find_one({"_id": ObjectId(edit_id)}) if edit_id else None
    
    material_list = list(db.materials.find())
    purchase_history = list(db.purchases.find().sort("date", -1))
    
    return render_template('purchase.html', 
                           material_list=material_list, 
                           purchase_history=purchase_history, 
                           edit_val=edit_val)
    
    

@app.route('/delete_purchase/<p_id>')
def delete_purchase(p_id):
    # This finds the specific purchase by ID and removes it
    db.purchases.delete_one({"_id": ObjectId(p_id)})
    # After deleting, it sends you back to the purchase list
    return redirect(url_for('purchase'))



@app.route('/dispatch', methods=['GET', 'POST'])
def dispatch():
    if request.method == 'POST':
        d_id = request.form.get('dispatch_id')
        # Use .strip() to remove accidental leading/trailing spaces
        material_name = request.form.get('material_name').strip()
        new_qty = float(request.form.get('qty') or 0)
        
        data = {
            "material_name": material_name,
            "qty": new_qty,
            "receiver": request.form.get('receiver'),
            "date": request.form.get('date'),
            "description": request.form.get('description')
        }
        
        if d_id:
            # 1. Reverse the previous stock change before updating
            old_dispatch = db.dispatches.find_one({"_id": ObjectId(d_id)})
            if old_dispatch:
                db.materials.update_one(
                    {"material_name": old_dispatch['material_name'].strip()},
                    {"$inc": {"qty": old_dispatch['qty']}}
                )
            
            # 2. Update the dispatch record
            db.dispatches.update_one({"_id": ObjectId(d_id)}, {"$set": data})
        else:
            # 3. Insert new dispatch record
            db.dispatches.insert_one(data)
        
        # 4. SUBTRACT from Inventory
        # We use $inc with a negative value. 
        # IMPORTANT: Ensure the material_name matches your materials collection exactly.
        result = db.materials.update_one(
            {"material_name": material_name},
            {"$inc": {"qty": -new_qty}}
        )

        # DEBUG: Check if the update actually happened
        if result.matched_count == 0:
            print(f"CRITICAL: Material '{material_name}' not found in Inventory collection!")
        
        return redirect(url_for('dispatch'))

    # GET Logic
    edit_id = request.args.get('edit_id')
    edit_val = db.dispatches.find_one({"_id": ObjectId(edit_id)}) if edit_id else None
    
    # Sort material list alphabetically for the dropdown
    material_list = list(db.materials.find().sort("material_name", 1))
    dispatch_history = list(db.dispatches.find().sort("date", -1))
    
    return render_template('dispatch.html', 
                           material_list=material_list, 
                           dispatch_history=dispatch_history, 
                           edit_val=edit_val)

@app.route('/delete_dispatch/<d_id>')
def delete_dispatch(d_id):
    dispatch_record = db.dispatches.find_one({"_id": ObjectId(d_id)})
    
    if dispatch_record:
        # ADD back the quantity to Inventory (canceling the dispatch)
        db.materials.update_one(
            {"material_name": dispatch_record['material_name'].strip()},
            {"$inc": {"qty": dispatch_record['qty']}}
        )
        
        # Delete the history record
        db.dispatches.delete_one({"_id": ObjectId(d_id)})
        
    return redirect(url_for('dispatch'))



@app.route('/delete_bill/<bill_id>')
def delete_bill(bill_id):
    if 'user' not in session: 
        return redirect(url_for('login'))
    
    target_bill = bills_col.find_one({"_id": ObjectId(bill_id)})
    if target_bill:
        p_ref = target_bill['project_ref']
        w_ref = target_bill['workorder_no']
        deleted_no = target_bill['bill_no']
        
        # Remove the specific bill
        bills_col.delete_one({"_id": ObjectId(bill_id)})
        
        # Shift all subsequent bills down by 1 to maintain sequence
        bills_col.update_many(
            {"project_ref": p_ref, "workorder_no": w_ref, "bill_no": {"$gt": deleted_no}},
            {"$inc": {"bill_no": -1}}
        )
        flash(f"RA Bill {deleted_no} deleted and sequence updated.")
        return redirect(url_for('billing', project_ref=p_ref, workorder_no=w_ref))
        
    return redirect(url_for('billing'))
    
    
@app.route('/delete_bom/<id>')
def delete_bom(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    bom_col.delete_one({"_id": ObjectId(id)})
    flash("BOM item removed.")
    return redirect(url_for('bom'))

# --- EDIT / DELETE ROUTES ---

@app.route('/edit_project/<id>', methods=['POST'])
def edit_project(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    updated_data = {
        "project_id": request.form['project_id'],
        "client_name": request.form['client_name'],
        "panel_type": request.form['panel_type'],
        "deadline": request.form['deadline']
    }
    
    projects_col.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
    flash("Project updated successfully!")
    return redirect(url_for('project'))

@app.route('/delete_project/<id>')
def delete_project(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    projects_col.delete_one({"_id": ObjectId(id)})
    flash("Project deleted.")
    return redirect(url_for('project'))

@app.route('/delete_boq/<id>')
def delete_boq(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    boq_col.delete_one({"_id": ObjectId(id)})
    flash("Entry removed from list.")
    return redirect(url_for('workorder'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
