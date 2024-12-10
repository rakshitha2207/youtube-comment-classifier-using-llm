HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>YouTube Comment Analyzer</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            background-color: #f8f9fa;
        }
        .main-container {
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
        }
        .input-section {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .chart-section {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            display: none;
        }
        .categories-section {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            display: none;
        }
        .category-btn {
            width: 100%;
            margin: 5px 0;
            text-align: left;
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .category-btn:hover {
            opacity: 0.9;
        }
        .comments-section {
            margin-top: 15px;
            display: none;
        }
        .comment-box {
            background: #f8f9fa;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            border-left: 4px solid #007bff;
        }
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        .count-badge {
            background: rgba(255,255,255,0.3);
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.9em;
        }
        .chart-container {
            position: relative;
            height: 300px;
            margin: 20px auto;
        }
        .error-message {
            color: #dc3545;
            margin-top: 10px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="main-container">
        <h1 class="text-center mb-4">YouTube Comment Analyzer</h1>
        
        <!-- Input Section -->
        <div class="input-section">
            <div class="form-group">
                <label for="video-url" class="form-label">Enter YouTube Video URL:</label>
                <div class="input-group">
                    <input type="text" class="form-control" id="video-url" 
                           placeholder="https://www.youtube.com/watch?v=...">
                    <button class="btn btn-primary" onclick="analyzeComments()">Analyze</button>
                </div>
            </div>
            <div id="error-display" class="error-message"></div>
        </div>

        <!-- Loading Indicator -->
        <div class="loading" id="loading">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2">Analyzing comments... Please wait.</p>
        </div>

        <!-- Results Section -->
        <div id="results">
            <!-- Chart Section -->
            <div class="chart-section" id="chart-section">
                <h4 class="text-center mb-3">Comment Distribution</h4>
                <div class="chart-container">
                    <canvas id="resultsChart"></canvas>
                </div>
            </div>

            <!-- Categories Section -->
            <div class="categories-section" id="categories-section">
                <h4 class="mb-3">Comment Categories</h4>
                
                <!-- All Comments -->
                <button class="category-btn btn btn-info text-white" onclick="toggleComments('all-comments')">
                    <span>All Comments</span>
                    <span id="all-comments-count" class="count-badge">0</span>
                </button>
                <div id="all-comments" class="comments-section"></div>

                <!-- Relevant Comments -->
                <button class="category-btn btn btn-primary" onclick="toggleComments('relevant-comments')">
                    <span>Relevant Comments</span>
                    <span id="relevant-comments-count" class="count-badge">0</span>
                </button>
                <div id="relevant-comments" class="comments-section"></div>

                <!-- Spam Comments -->
                <button class="category-btn btn btn-warning" onclick="toggleComments('spam-comments')">
                    <span>Spam Comments</span>
                    <span id="spam-comments-count" class="count-badge">0</span>
                </button>
                <div id="spam-comments" class="comments-section"></div>

                <!-- Appreciation Comments -->
                <button class="category-btn btn btn-success" onclick="toggleComments('appreciation-comments')">
                    <span>Appreciation Comments</span>
                    <span id="appreciation-comments-count" class="count-badge">0</span>
                </button>
                <div id="appreciation-comments" class="comments-section"></div>

                <!-- Grievance Comments -->
                <button class="category-btn btn btn-danger" onclick="toggleComments('grievance-comments')">
                    <span>Grievance Comments</span>
                    <span id="grievance-comments-count" class="count-badge">0</span>
                </button>
                <div id="grievance-comments" class="comments-section"></div>
            </div>
        </div>
    </div>

    <script>
        let resultsChart = null;

        function toggleComments(elementId) {
            // Hide all comment sections
            document.querySelectorAll('.comments-section').forEach(section => {
                section.style.display = 'none';
            });
            
            // Show the selected section
            const selectedSection = document.getElementById(elementId);
            selectedSection.style.display = selectedSection.style.display === 'block' ? 'none' : 'block';
        }

        function displayResults(data) {
            // Show results sections
            document.getElementById('chart-section').style.display = 'block';
            document.getElementById('categories-section').style.display = 'block';
            
            // Update comment counts
            document.getElementById('all-comments-count').textContent = Object.values(data).flat().length;
            document.getElementById('relevant-comments-count').textContent = data.relevant.length;
            document.getElementById('spam-comments-count').textContent = data.spam.length;
            document.getElementById('appreciation-comments-count').textContent = data.appreciation.length;
            document.getElementById('grievance-comments-count').textContent = data.grievance.length;
            
            // Display comments
            displayComments('all-comments', Object.values(data).flat());
            displayComments('relevant-comments', data.relevant);
            displayComments('spam-comments', data.spam);
            displayComments('appreciation-comments', data.appreciation);
            displayComments('grievance-comments', data.grievance);
            
            // Update chart
            updateChart(data);
        }

        function updateChart(data) {
            const ctx = document.getElementById('resultsChart').getContext('2d');
            
            if (resultsChart) {
                resultsChart.destroy();
            }
            
            const total = Object.values(data).flat().length;
            
            resultsChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['Relevant', 'Spam', 'Appreciation', 'Grievance'],
                    datasets: [{
                        data: [
                            data.relevant.length,
                            data.spam.length,
                            data.appreciation.length,
                            data.grievance.length
                        ],
                        backgroundColor: [
                            'rgba(0, 123, 255, 0.8)',
                            'rgba(255, 193, 7, 0.8)',
                            'rgba(40, 167, 69, 0.8)',
                            'rgba(220, 53, 69, 0.8)'
                        ],
                        borderColor: [
                            'rgb(0, 123, 255)',
                            'rgb(255, 193, 7)',
                            'rgb(40, 167, 69)',
                            'rgb(220, 53, 69)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const value = context.raw;
                                    const percentage = ((value / total) * 100).toFixed(1);
                                    return ${context.label}: ${value} (${percentage}%);
                                }
                            }
                        }
                    }
                }
            });
        }

        function displayComments(elementId, comments) {
            const container = document.getElementById(elementId);
            container.innerHTML = '';
            
            if (!comments || comments.length === 0) {
                container.innerHTML = '<p class="text-muted">No comments in this category</p>';
                return;
            }

            comments.forEach(comment => {
                const div = document.createElement('div');
                div.className = 'comment-box';
                div.textContent = comment;
                container.appendChild(div);
            });
        }

        function showError(message) {
            const errorDisplay = document.getElementById('error-display');
            errorDisplay.textContent = message;
            errorDisplay.style.display = 'block';
            setTimeout(() => {
                errorDisplay.style.display = 'none';
            }, 5000);
        }

        function analyzeComments() {
            const videoUrl = document.getElementById('video-url').value;
            if (!videoUrl) {
                showError('Please enter a YouTube video URL');
                return;
            }

            // Show loading spinner
            document.getElementById('loading').style.display = 'block';
            document.getElementById('chart-section').style.display = 'none';
            document.getElementById('categories-section').style.display = 'none';
            document.getElementById('error-display').style.display = 'none';

            // Make API request
            fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    video_url: videoUrl
                })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('loading').style.display = 'none';
                
                if (data.error) {
                    showError(data.error);
                    return;
                }
                
                displayResults(data);
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('loading').style.display = 'none';
                showError('An error occurred while analyzing comments: ' + error.message);
            });
        }
    </script>
</body>
</html>
"""  