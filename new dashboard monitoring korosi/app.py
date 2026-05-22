from flask import Flask, render_template, request, url_for, redirect
import os
import time
from logic_engine import calculate_life, get_status_action, CorrosionAI
import cloudinary
import cloudinary.uploader
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Cloudinary Configuration
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# Supabase Configuration
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

ai = CorrosionAI()

@app.route('/')
def index():
    # Fetch data from Supabase
    response = supabase.table('corrosion_reports').select("*").order('created_at', desc=True).execute()
    items = response.data
    return render_template('index.html', items=items)

@app.route('/graphics')
def graphics():
    # Fetch data from Supabase for graphics
    response = supabase.table('corrosion_reports').select("*").execute()
    items = response.data
    
    # Aggregate Status data for Pie Chart
    status_counts = {'Aman': 0, 'Waspada': 0, 'Kritis': 0}
    for item in items:
        if item['status'] in status_counts:
            status_counts[item['status']] += 1
    
    # Aggregate Accessories data for Bar Chart
    acc_counts = {}
    for item in items:
        acc = item['accessory']
        acc_counts[acc] = acc_counts.get(acc, 0) + 1
    
    return render_template('graphics.html', 
                           status_data=status_counts, 
                           acc_data=acc_counts)

@app.route('/input', methods=['POST'])
def handle_input():
    tower = request.form.get('tower')
    circuit = request.form.get('circuit')
    accessory = request.form.get('accessory')
    date = request.form.get('date')
    level = request.form.get('level')
    photo = request.files.get('photo')

    if photo:
        # Save temporarily to analyze
        filename = f"{int(time.time())}_{photo.filename}"
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(temp_path)
        
        # AI Analysis
        perc = ai.analyze_image(temp_path)
        
        # Calculation Logic
        life_val = calculate_life(level, perc)
        status, color_class, action = get_status_action(perc)
        
        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(temp_path)
        image_url = upload_result['secure_url']
        public_id = upload_result['public_id']
        
        # Remove temporary file
        os.remove(temp_path)
        
        # Save to Supabase
        data = {
            'tower_id': tower,
            'circuit': circuit,
            'accessory': accessory,
            'date': date,
            'level': level,
            'ai_percentage': perc,
            'remaining_life': f"{life_val:.1f} Tahun",
            'status': status,
            'color': color_class,
            'action': action,
            'image_url': image_url,
            'public_id': public_id
        }
        supabase.table('corrosion_reports').insert(data).execute()

    return redirect(url_for('index'))

@app.route('/delete/<string:public_id>', methods=['POST'])
def delete_item(public_id):
    # Remove from Supabase
    supabase.table('corrosion_reports').delete().eq('public_id', public_id).execute()
    
    # Remove from Cloudinary
    cloudinary.uploader.destroy(public_id)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
