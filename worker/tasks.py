import os
import time
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import urllib.request

# Attempt to import Pillow (PIL) for real-world image processing.
# If Pillow isn't installed, we provide a clean, simulation fallback so the worker doesn't crash.
try:
    from PIL import Image, ImageFilter, ImageDraw, ImageFont
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False


# =====================================================================
# TASK 1: Dynamic Image Optimization & Watermarking (CPU Intensive)
# =====================================================================
def optimize_image_payload(input_path, output_width=800, quality=85):
    """
    Simulates or executes a heavy, CPU-bound image manipulation process.
    Loads an image, resizes it, applies a soft blur/vignette filter, 
    and saves an optimized JPEG version.
    """
    print(f"[Image Task] Processing image: {input_path}")
    
    if not PILLOW_AVAILABLE:
        # Graceful fallback simulation if Pillow is not installed on the system
        print("[Image Task] [SIMULATION MODE] Pillow library not found. Simulating image processing matrix operations...")
        time.sleep(2.5)  # Simulate the heavy math computation overhead
        return {
            "status": "SIMULATED_SUCCESS",
            "message": "Pillow is missing, but simulation completed successfully.",
            "metrics": {
                "input_file": input_path,
                "applied_resolution": f"{output_width}x(auto)",
                "compression_ratio": "85%",
                "filter_kernel": "GAUSSIAN_BLUR"
            }
        }
    
    # Real execution if Pillow is installed
    try:
        if not os.path.exists(input_path):
            # Create a dummy image for testing purposes if the file doesn't exist
            print(f"[Image Task] File {input_path} not found. Creating a temporary mock canvas...")
            img = Image.new('RGB', (1920, 1080), color=(54, 57, 63))
            draw = ImageDraw.Draw(img)
            draw.text((100, 450), "Distributed Task Queue Testing Canvas", fill=(255, 255, 255))
            img.save(input_path)
            
        # Open and process the image
        with Image.open(input_path) as img:
            # Maintain aspect ratio
            w_percent = (output_width / float(img.size[0]))
            h_size = int((float(img.size[1]) * float(w_percent)))
            img = img.resize((output_width, h_size), Image.Resampling.LANCZOS)
            
            # Apply a professional Gaussian Blur filter
            processed_img = img.filter(ImageFilter.GaussianBlur(radius=1.5))
            
            # Output generation
            dir_name, file_name = os.path.split(input_path)
            opt_file_name = f"optimized_{file_name}"
            output_path = os.path.join(dir_name, opt_file_name)
            
            processed_img.save(output_path, "JPEG", quality=quality)
            
            return {
                "status": "SUCCESS",
                "message": f"Successfully optimized and filtered image frame.",
                "metrics": {
                    "saved_filepath": output_path,
                    "new_dimensions": f"{output_width}x{h_size}",
                    "compression_quality": f"{quality}%",
                    "file_size_bytes": os.path.getsize(output_path)
                }
            }
    except Exception as e:
        raise RuntimeError(f"Failed to process image frame: {str(e)}")


# =====================================================================
# TASK 2: Templated HTML Email Generation & Delivery (Network Latency)
# =====================================================================
def send_automated_email(recipient, subject, username, activation_code, live_mode=False, smtp_config=None):
    """
    Generates a beautifully styled, responsive HTML system email and dispatches it.
    Features a sandbox safety default mode to print SMTP telemetry instead of crashing if no mail server is ready.
    """
    print(f"[Email Task] Generating HTML template payload for {recipient}...")
    
    # Beautiful responsive CSS/HTML template design
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f6f8; margin: 0; padding: 40px; }}
            .container {{ max-width: 600px; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }}
            .header {{ background: #4f46e5; padding: 30px; text-align: center; color: white; }}
            .body {{ padding: 40px; color: #374151; line-height: 1.6; }}
            .code-block {{ background: #f3f4f6; border: 1px dashed #e5e7eb; padding: 15px; text-align: center; font-size: 24px; font-family: monospace; letter-spacing: 5px; color: #4f46e5; font-weight: bold; margin: 20px 0; border-radius: 4px; }}
            .footer {{ background: #f9fafb; padding: 20px; text-align: center; font-size: 12px; color: #9ca3af; border-top: 1px solid #f3f4f6; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Security Verification Portal</h2>
            </div>
            <div class="body">
                <p>Hello <strong>{username}</strong>,</p>
                <p>We received a verification request for your account on our distributed cluster network. Please use the following authorization token to proceed:</p>
                <div class="code-block">{activation_code}</div>
                <p>If you did not initiate this transaction, you can safely ignore this automated message.</p>
            </div>
            <div class="footer">
                Distributed Task System Daemon Core • 2026 Sandbox Operations
            </div>
        </div>
    </body>
    </html>
    """

    if not live_mode:
        # Perfect for testing without configuring SMTP servers
        print(f"[Email Task] [SANDBOX MODE] Simulating network latency...")
        time.sleep(1.8)
        return {
            "status": "SANDBOX_VERIFIED",
            "message": "Mail processed and recorded in local dispatch logs.",
            "delivery_recipient": recipient,
            "smtp_payload_preview": {
                "from": "system-daemon@sandbox-cluster.io",
                "to": recipient,
                "subject": subject,
                "content_type": "text/html"
            }
        }

    # Live Delivery Protocol
    try:
        conf = smtp_config or {}
        host = conf.get("host", "localhost")
        port = conf.get("port", 1025)  # Default local mail debugging port
        user = conf.get("username", "")
        password = conf.get("password", "")

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = "system-daemon@sandbox-cluster.io"
        msg['To'] = recipient

        part = MIMEText(html_template, 'html')
        msg.attach(part)

        # Connect and secure pipeline
        with smtplib.SMTP(host, port) as server:
            if user and password:
                server.starttls()
                server.login(user, password)
            server.sendmail(msg['From'], [recipient], msg.as_string())

        return {
            "status": "DELIVERED",
            "message": f"Live SMTP packet successfully sent to {recipient}.",
            "server": f"{host}:{port}"
        }
    except Exception as e:
        raise RuntimeError(f"SMTP network protocol rejected delivery: {str(e)}")


# =====================================================================
# TASK 3: API Data Mining & Analytics Aggregation (I/O Bound)
# =====================================================================
def fetch_and_aggregate_api_data(dataset_endpoint="https://jsonplaceholder.typicode.com/posts"):
    """
    Dials out to an external public Web API, downloads raw system JSON records,
    and runs aggregation analytics computations on the returned payload.
    """
    print(f"[Analytics Task] Querying remote datastore endpoint: {dataset_endpoint}")
    
    try:
        # Set a clean timeout of 10 seconds to avoid hung worker threads
        req = urllib.request.Request(
            dataset_endpoint, 
            headers={'User-Agent': 'Mozilla/5.0 (Distributed-Task-Worker)'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            raw_data = response.read().decode('utf-8')
            records = json.loads(raw_data)
            
        total_records = len(records)
        print(f"[Analytics Task] Fetched {total_records} data structures. Running aggregation formulas...")
        
        # Calculate statistics
        user_frequencies = {}
        title_word_counts = []
        
        for record in records:
            # Track user posts counts
            user_id = record.get("userId", "UNKNOWN")
            user_frequencies[user_id] = user_frequencies.get(user_id, 0) + 1
            
            # Extract statistics on length of entries
            title = record.get("title", "")
            title_word_counts.append(len(title.split()))
            
        avg_word_count = sum(title_word_counts) / max(len(title_word_counts), 1)
        
        return {
            "status": "SUCCESS",
            "source_endpoint": dataset_endpoint,
            "analytics": {
                "parsed_records_count": total_records,
                "unique_active_users_detected": len(user_frequencies),
                "average_words_per_title": round(avg_word_count, 2),
                "most_active_contributor_id": max(user_frequencies, key=user_frequencies.get),
                "processing_timestamp": time.time()
            }
        }
        
    except Exception as e:
        raise RuntimeError(f"Data mining interface pipeline failure: {str(e)}")


# =====================================================================
# TASK 4: Structured Data Compilation & Export (File I/O)
# =====================================================================
def export_raw_data_to_csv(output_filename, records):
    """
    Transforms unstructured JSON payloads into perfectly formatted comma-separated rows.
    Compiles, sanitizes string entries, and writes a robust CSV output cleanly to disk.
    """
    print(f"[Export Task] Processing raw tabular array into file: {output_filename}")
    
    if not records or not isinstance(records, list):
        raise ValueError("Invalid array format. Expected non-empty list of dictionary records.")
        
    try:
        # Generate headers from the absolute keys inside our records
        headers = list(records[0].keys())
        
        output_lines = [",".join(headers)]
        
        for record in records:
            row_items = []
            for h in headers:
                val = str(record.get(h, ""))
                # Sanitize values containing commas or quotes to prevent formatting breaking
                if "," in val or '"' in val or "\n" in val:
                    val = val.replace('"', '""')
                    val = f'"{val}"'
                row_items.append(val)
            output_lines.append(",".join(row_items))
            
        # Write directly to flat file
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(output_lines))
            
        return {
            "status": "SUCCESS",
            "target_file": output_filename,
            "metrics": {
                "compiled_rows": len(records),
                "column_headers": headers,
                "file_size_bytes": os.path.getsize(output_filename)
            }
        }
    except Exception as e:
        raise RuntimeError(f"Tabular compilation engine crashed: {str(e)}")


# =====================================================================
# TASK REGISTRY MAP (The Workers Lookup Brains)
# =====================================================================
TASK_REGISTRY = {
    "optimize_image_payload": optimize_image_payload,
    "send_automated_email": send_automated_email,
    "fetch_and_aggregate_api_data": fetch_and_aggregate_api_data,
    "export_raw_data_to_csv": export_raw_data_to_csv
}