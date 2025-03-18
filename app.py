from flask import Flask, render_template, request

app = Flask(__name__)

# Helper functions
def trim_text_to_middle_segment(text, target_words):
    """Trim text to a middle segment of target_words length."""
    words = text.split()
    total_words = len(words)
    if total_words <= target_words:
        return text
    start_index = (total_words - target_words) // 2
    end_index = start_index + target_words
    trimmed_words = words[start_index:end_index]
    return ' '.join(trimmed_words)

def get_target_words():
    """Return target word count for 60 seconds of audio."""
    return 150  # Assuming 150 words = 60 seconds

# Frontend route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        # Estimate audio length (0.4 seconds per word)
        num_words = len(text.split())
        estimated_time = num_words * 0.4
        # Trim text if estimated time exceeds 60 seconds
        if estimated_time > 60:
            target_words = get_target_words()
            trimmed_text = trim_text_to_middle_segment(text, target_words)
        else:
            trimmed_text = text
        return render_template('index.html', 
                             original_text=text, 
                             trimmed_text=trimmed_text, 
                             estimated_time=estimated_time)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)