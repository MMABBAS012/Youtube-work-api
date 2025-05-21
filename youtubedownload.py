from flask import Flask, request, send_file, jsonify
from pytube import YouTube
import os
import tempfile

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400
    
    try:
        yt = YouTube(url)
        # Get highest resolution progressive stream (video + audio)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        if not stream:
            return jsonify({"error": "No suitable video streams found"}), 404
        
        # Download to a temp file
        temp_dir = tempfile.gettempdir()
        out_file = stream.download(output_path=temp_dir)
        
        # Send file to user
        return send_file(out_file, as_attachment=True, download_name=f"{yt.title}.mp4")
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)