from flask import Flask, render_template_string, request, jsonify, send_file
import requests
import base64
import io

app = Flask(__name__)

# ==========================================
# CONFIGURATION
# ==========================================
DEEPSWAP_API = "https://api.deepswapper.com/swap"
# Credits: @aaka8h
SECURITY_PAYLOAD = {
    "token": "0.ufDEMbVMT7mc9_XLsFDSK5CQqdj9Cx_Zjww0DevIvXN5M4fXQr3B9YtPdGkKAHjXBK6UC9rFcEbZbzCfkxxgmdTYV8iPzTby0C03dTKv5V9uXFYfwIVlqwNbIsfOK_rLRHIPB31bQ0ijSTEd-lLbllf3MkEcpkEZFFmmq8HMAuRuliCXFEdCwEB1HoYSJtvJEmDIVsooU3gYdrCm5yOJ8_lZ4DiHCSvy7P8-YxwJKkapJNCMUCFIfJbWDkDzvh8DGPyTRoHbURX8kClfImmPrGcqlfd7kkoNRcudS25IbNf1CGBsh8V96MtEhnTZvOpZfnp5dpV7MfgwOgvx7hUazUaC_wxQE63Aa0uOPuGvJ70BNrmeZIIrY9roD1Koj316L4g2BZ_LLZZF11wcrNNon8UXB0iVudiNCJyDQCxLUmblXUpt4IUvRoiOqXBNtWtLqY0su0ieVB0jjyDf_-zs7wc8WQ_jqp-NsTxgKOgvZYWV6Elz_lf4cNxGHZJ5BdcyLEoRBH3cksvwoncmYOy5Ulco22QT-x2z06xVFBZYZMVulxAcmvQemKfSFKsNaDxwor35p-amn9Vevhyb-GzA_oIoaTmc0fVXSshax2rdFQHQms86fZ_jkTieRpyIuX0mI3C5jLGIiOXzWxNgax9eZeQstYjIh8BIdMiTIUHfyKVTgtoLbK0hjTUTP0xDlCLnOt5qHdwe_iTWedBsswAJWYdtIxw0YUfIU22GMYrJoekOrQErawNlU5yT-LhXquBQY3EBtEup4JMWLendSh68d6HqjN2T3sAfVw0nY5jg7_5LJwj5gqEk57devNN8GGhogJpfdGzYoNGja22IZIuDnPPmWTpGx4VcLOLknSHrzio.tXUN6eooS69z3QtBp-DY1g.d882822dfe05be2b36ed1950554e1bac753abfe304a289adc4289b3f0d517356",
    "type": "invisible",
    "id": "deepswapper"
}

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>AI Face Swap | @aaka8h</title>
    <meta name="author" content="@aaka8h">
    <link rel="icon" href="https://files.catbox.moe/gt0b6x.jpg" />
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet" />
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@300;400;600&display=swap" rel="stylesheet" />
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>

    <style>
        :root {
            --bg-dark: #020408;
            --glass-bg: rgba(13, 17, 28, 0.85);
            --glass-border: rgba(255, 255, 255, 0.08);
            --primary-gradient: linear-gradient(135deg, #6366f1 0%, #d946ef 100%);
            --accent-glow: rgba(99, 102, 241, 0.25);
            --text-main: #f1f5f9;
            --text-dim: #94a3b8;
        }

        body {
            background-color: var(--bg-dark);
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(217, 70, 239, 0.15) 0px, transparent 50%);
            background-attachment: fixed;
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            overflow-x: hidden;
        }

        .brand-font { font-family: 'Outfit', sans-serif; font-weight: 700; }

        /* --- Navbar --- */
        .navbar {
            backdrop-filter: blur(20px);
            background: rgba(2, 4, 8, 0.8);
            border-bottom: 1px solid var(--glass-border);
            padding: 1rem 0;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .credits-badge {
            background: rgba(255,255,255,0.1);
            border: 1px solid var(--glass-border);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* --- Auth & App Container --- */
        .view-section {
            display: none; /* Hidden by default */
            animation: fadeIn 0.5s ease;
        }
        
        .view-section.active { display: block; }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        .glass-panel {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 2.5rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
        }

        /* --- Forms --- */
        .form-control {
            background: rgba(255,255,255,0.05);
            border: 1px solid var(--glass-border);
            color: white;
            padding: 12px 20px;
            border-radius: 12px;
        }
        .form-control:focus {
            background: rgba(255,255,255,0.1);
            border-color: #6366f1;
            color: white;
            box-shadow: none;
        }

        /* --- Buttons --- */
        .btn-gradient {
            background: var(--primary-gradient);
            border: none;
            color: white;
            padding: 12px;
            border-radius: 50px;
            font-weight: 700;
            width: 100%;
            transition: 0.3s;
            box-shadow: 0 0 20px var(--accent-glow);
        }
        .btn-gradient:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 0 30px var(--accent-glow); }
        .btn-gradient:disabled { opacity: 0.6; cursor: not-allowed; }

        /* --- Upload Zones --- */
        .upload-zone {
            border: 2px dashed var(--glass-border);
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            background: rgba(255, 255, 255, 0.02);
            position: relative;
            min-height: 250px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            transition: 0.3s;
        }
        .upload-zone:hover { border-color: #818cf8; background: rgba(99, 102, 241, 0.05); }
        .upload-zone img { width: 100%; height: 100%; object-fit: contain; position: absolute; top:0; left:0; padding:10px; }

        /* --- History --- */
        .history-card {
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            overflow: hidden;
            position: relative;
            aspect-ratio: 1;
        }
        .history-card img { width: 100%; height: 100%; object-fit: cover; }
        
        .remove-btn {
            position: absolute; top: 10px; right: 10px; z-index: 10;
            background: rgba(220, 38, 38, 0.9); color: white; border: none;
            width: 30px; height: 30px; border-radius: 50%; display: none;
        }

        /* --- Loading --- */
        .loading-overlay {
            position: fixed; inset: 0; background: rgba(2,4,8,0.95);
            display: none; justify-content: center; align-items: center; z-index: 999;
            flex-direction: column;
        }
        .spinner {
            width: 60px; height: 60px; border: 4px solid rgba(255,255,255,0.1);
            border-left-color: #d946ef; border-radius: 50%; animation: spin 1s linear infinite;
        }
        @keyframes spin { 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>

    <div id="loader" class="loading-overlay">
        <div class="spinner mb-4"></div>
        <h4 class="brand-font">Processing Magic...</h4>
    </div>

    <nav class="navbar" id="appNavbar" style="display: none;">
        <div class="container">
            <a class="navbar-brand brand-font text-white" href="#">
                <i class="fas fa-bolt text-warning me-2"></i>AB SWAP
            </a>
            <div class="d-flex align-items-center gap-3">
                <div class="credits-badge">
                    <i class="fas fa-coins text-warning"></i>
                    <span id="creditDisplay">0 Credits</span>
                </div>
                <div class="dropdown">
                    <button class="btn btn-sm btn-outline-light rounded-pill dropdown-toggle" type="button" data-bs-toggle="dropdown">
                        <i class="fas fa-user-circle me-1"></i> <span id="usernameDisplay">User</span>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-dark">
                        <li><a class="dropdown-item" href="#" onclick="logout()"><i class="fas fa-sign-out-alt me-2"></i>Logout</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </nav>

    <div class="container py-5">
        
        <div id="authView" class="view-section active">
            <div class="row justify-content-center">
                <div class="col-md-5">
                    <div class="text-center mb-5">
                        <h1 class="brand-font display-4 mb-2">AB Face Swap</h1>
                        <p class="text-dim">Next Gen AI Tools by <a href="https://t.me/aaka8h" class="text-info text-decoration-none">@aaka8h</a></p>
                    </div>

                    <div class="glass-panel">
                        <div id="loginForm">
                            <h3 class="brand-font mb-4">Welcome Back</h3>
                            <form onsubmit="handleLogin(event)">
                                <div class="mb-3">
                                    <label class="text-dim small text-uppercase fw-bold">Username</label>
                                    <input type="text" id="loginUser" class="form-control" required placeholder="Enter username" autocomplete="off">
                                </div>
                                <div class="mb-4">
                                    <label class="text-dim small text-uppercase fw-bold">Password</label>
                                    <input type="password" id="loginPass" class="form-control" required placeholder="Enter password">
                                </div>
                                <button type="submit" class="btn-gradient mb-3">Login</button>
                                <p class="text-center text-dim">
                                    New here? <a href="#" class="text-white fw-bold" onclick="toggleAuth('signup')">Create Account</a>
                                </p>
                                <div class="text-center mt-4 pt-3 border-top border-secondary border-opacity-25">
                                    <button type="button" onclick="factoryReset()" class="btn btn-sm btn-outline-danger border-0">
                                        <i class="fas fa-trash-alt me-1"></i> Reset App Data
                                    </button>
                                </div>
                            </form>
                        </div>

                        <div id="signupForm" style="display: none;">
                            <h3 class="brand-font mb-4">Create Account</h3>
                            <div class="alert alert-info py-2 small"><i class="fas fa-gift me-2"></i>Get 5 Free Credits on Signup!</div>
                            <form onsubmit="handleSignup(event)">
                                <div class="mb-3">
                                    <label class="text-dim small text-uppercase fw-bold">Choose Username</label>
                                    <input type="text" id="signupUser" class="form-control" required autocomplete="off">
                                </div>
                                <div class="mb-4">
                                    <label class="text-dim small text-uppercase fw-bold">Choose Password</label>
                                    <input type="password" id="signupPass" class="form-control" required>
                                </div>
                                <button type="submit" class="btn-gradient mb-3">Sign Up</button>
                                <p class="text-center text-dim">
                                    Have an account? <a href="#" class="text-white fw-bold" onclick="toggleAuth('login')">Login</a>
                                </p>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div id="appView" class="view-section">
            <div class="row justify-content-center">
                <div class="col-lg-10">
                    
                    <div class="glass-panel mb-4">
                        <form id="swapForm">
                            <div class="row g-4">
                                <div class="col-md-6">
                                    <label class="text-uppercase text-dim small fw-bold mb-2 ms-1">Source Face</label>
                                    <div class="upload-zone" id="zone-source" onclick="triggerUpload('source')">
                                        <input type="file" id="source" name="source" accept="image/*" hidden onchange="previewImage(this, 'source')">
                                        <div class="text-center" id="info-source">
                                            <i class="fas fa-user-circle fa-3x mb-3 text-secondary"></i>
                                            <p class="mb-1 fw-bold">Select Face</p>
                                        </div>
                                        <img id="preview-source" style="display:none">
                                        <button type="button" class="remove-btn" id="btn-rm-source" onclick="removeImage(event, 'source')">
                                            <i class="fas fa-times"></i>
                                        </button>
                                    </div>
                                </div>

                                <div class="col-md-6">
                                    <label class="text-uppercase text-dim small fw-bold mb-2 ms-1">Target Photo</label>
                                    <div class="upload-zone" id="zone-target" onclick="triggerUpload('target')">
                                        <input type="file" id="target" name="target" accept="image/*" hidden onchange="previewImage(this, 'target')">
                                        <div class="text-center" id="info-target">
                                            <i class="fas fa-image fa-3x mb-3 text-secondary"></i>
                                            <p class="mb-1 fw-bold">Select Target</p>
                                        </div>
                                        <img id="preview-target" style="display:none">
                                        <button type="button" class="remove-btn" id="btn-rm-target" onclick="removeImage(event, 'target')">
                                            <i class="fas fa-times"></i>
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <div class="mt-4 pt-2">
                                <button type="submit" class="btn-gradient" id="submitBtn" disabled>
                                    <i class="fas fa-wand-magic-sparkles me-2"></i> Swap Faces (1 Credit)
                                </button>
                            </div>
                        </form>
                    </div>

                    <div id="resultSection" style="display: none;">
                        <div class="glass-panel text-center">
                            <h3 class="brand-font mb-4 text-success">Swap Successful!</h3>
                            <img id="resultImage" class="img-fluid rounded-4 shadow-lg mb-4" style="max-height: 500px;">
                            <div class="d-flex justify-content-center gap-3">
                                <a id="downloadLink" href="#" class="btn btn-light rounded-pill px-4 fw-bold">Download</a>
                                <button onclick="resetSwap()" class="btn btn-outline-light rounded-pill px-4">New Swap</button>
                            </div>
                        </div>
                    </div>

                    <div class="mt-5">
                        <h4 class="brand-font mb-4"><i class="fas fa-history me-2 text-dim"></i>My History</h4>
                        <div class="row g-3" id="historyGrid"></div>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <footer class="text-center py-4 text-dim border-top border-secondary border-opacity-25 mt-5">
        <p class="mb-0">Designed & Secured by <a href="https://t.me/aaka8h" class="text-info text-decoration-none">@aaka8h</a></p>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>

    <script>
        // ==========================================
        // LOCAL DATABASE LOGIC (Vercel Compatible)
        // ==========================================
        const DB = {
            getUsers: () => {
                try {
                    return JSON.parse(localStorage.getItem('ab_users') || '[]');
                } catch(e) {
                    console.error("Data Corrupted", e);
                    return [];
                }
            },
            saveUsers: (users) => localStorage.setItem('ab_users', JSON.stringify(users)),
            getCurrentUser: () => JSON.parse(localStorage.getItem('ab_current_user')),
            setCurrentUser: (user) => localStorage.setItem('ab_current_user', JSON.stringify(user)),
            logout: () => localStorage.removeItem('ab_current_user')
        };

        let currentUser = null;

        // --- Auth Functions ---
        function initApp() {
            currentUser = DB.getCurrentUser();
            if (currentUser) {
                showApp();
            } else {
                showAuth();
            }
        }

        function toggleAuth(view) {
            // Clear inputs
            document.getElementById('loginUser').value = '';
            document.getElementById('loginPass').value = '';
            document.getElementById('signupUser').value = '';
            document.getElementById('signupPass').value = '';
            
            if (view === 'signup') {
                document.getElementById('loginForm').style.display = 'none';
                document.getElementById('signupForm').style.display = 'block';
            } else {
                document.getElementById('signupForm').style.display = 'none';
                document.getElementById('loginForm').style.display = 'block';
            }
        }

        function factoryReset() {
            if(confirm("This will delete ALL accounts and data from this browser. Are you sure?")) {
                localStorage.clear();
                location.reload();
            }
        }

        function handleSignup(e) {
            e.preventDefault();
            // FIX: Force Lowercase to prevent Case Sensitivity Issues
            const u = document.getElementById('signupUser').value.trim().toLowerCase();
            const p = document.getElementById('signupPass').value.trim();
            
            if(u.length < 3) {
                Swal.fire('Error', 'Username must be at least 3 characters', 'error');
                return;
            }

            const users = DB.getUsers();
            if (users.find(user => user.username === u)) {
                Swal.fire('Error', 'Username already taken!', 'error');
                return;
            }

            const newUser = { username: u, password: p, credits: 5, history: [] };
            users.push(newUser);
            DB.saveUsers(users);
            
            console.log("Registered:", u); // Debug log
            
            Swal.fire('Success', 'Account created! You got 5 free credits.', 'success')
                .then(() => toggleAuth('login'));
        }

        function handleLogin(e) {
            e.preventDefault();
            // FIX: Force Lowercase to match stored data
            const u = document.getElementById('loginUser').value.trim().toLowerCase();
            const p = document.getElementById('loginPass').value.trim();

            const users = DB.getUsers();
            console.log("Attempting Login:", u); // Debug log
            console.log("Stored Users:", users.map(user => user.username)); // Debug log

            const user = users.find(usr => usr.username === u && usr.password === p);

            if (user) {
                DB.setCurrentUser(user);
                currentUser = user;
                showApp();
                Swal.fire({
                    toast: true, position: 'top-end', showConfirmButton: false,
                    timer: 3000, icon: 'success', title: `Welcome back, ${u}!`
                });
            } else {
                Swal.fire('Error', 'Invalid username or password. Check console (F12) for debugging.', 'error');
            }
        }

        function logout() {
            DB.logout();
            location.reload();
        }

        // --- App UI Functions ---
        function showApp() {
            document.getElementById('authView').classList.remove('active');
            document.getElementById('appView').classList.add('active');
            document.getElementById('appNavbar').style.display = 'block';
            updateProfileUI();
            renderHistory();
        }

        function showAuth() {
            document.getElementById('appView').classList.remove('active');
            document.getElementById('authView').classList.add('active');
            document.getElementById('appNavbar').style.display = 'none';
        }

        function updateProfileUI() {
            if(!currentUser) return;
            document.getElementById('usernameDisplay').innerText = currentUser.username;
            document.getElementById('creditDisplay').innerText = `${currentUser.credits} Credits`;
        }

        function triggerUpload(id) { document.getElementById(id).click(); }

        function previewImage(input, id) {
            if (input.files && input.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById(`preview-${id}`).src = e.target.result;
                    document.getElementById(`preview-${id}`).style.display = 'block';
                    document.getElementById(`info-${id}`).style.display = 'none';
                    document.getElementById(`btn-rm-${id}`).style.display = 'block';
                    checkForm();
                }
                reader.readAsDataURL(input.files[0]);
            }
        }

        function removeImage(e, id) {
            e.stopPropagation();
            document.getElementById(id).value = '';
            document.getElementById(`preview-${id}`).style.display = 'none';
            document.getElementById(`info-${id}`).style.display = 'block';
            document.getElementById(`btn-rm-${id}`).style.display = 'none';
            checkForm();
        }

        function checkForm() {
            const s = document.getElementById('source').value;
            const t = document.getElementById('target').value;
            document.getElementById('submitBtn').disabled = !(s && t);
        }

        // --- Swap Logic ---
        document.getElementById('swapForm').addEventListener('submit', async (e) => {
            e.preventDefault();

            if (currentUser.credits < 1) {
                Swal.fire('Low Balance', 'You have 0 credits! Contact @aaka8h for refill.', 'warning');
                return;
            }

            const loader = document.getElementById('loader');
            loader.style.display = 'flex';
            
            const formData = new FormData(e.target);

            try {
                const response = await fetch('/swap', { method: 'POST', body: formData });
                if (!response.ok) throw new Error('API Error');

                const blob = await response.blob();
                const reader = new FileReader();
                reader.readAsDataURL(blob);
                
                reader.onloadend = function() {
                    const resultBase64 = reader.result;
                    
                    // 1. Deduct Credit & Save History
                    updateUserData(resultBase64);

                    // 2. Show Result
                    document.getElementById('resultImage').src = resultBase64;
                    document.getElementById('downloadLink').href = resultBase64;
                    document.getElementById('downloadLink').download = `swap_${Date.now()}.png`;
                    
                    document.getElementById('swapForm').style.display = 'none';
                    document.getElementById('resultSection').style.display = 'block';
                    loader.style.display = 'none';
                    
                    Swal.fire('Magic!', 'Face swapped successfully.', 'success');
                }
            } catch (error) {
                loader.style.display = 'none';
                Swal.fire('Failed', 'Something went wrong. Try again.', 'error');
            }
        });

        function updateUserData(imgData) {
            // Update local object
            currentUser.credits -= 1;
            currentUser.history.unshift(imgData);
            if(currentUser.history.length > 6) currentUser.history.pop(); // Keep last 6

            // Save to DB (Local Storage)
            DB.setCurrentUser(currentUser); // Update session
            
            // Update Main User DB
            const allUsers = DB.getUsers();
            const index = allUsers.findIndex(u => u.username === currentUser.username);
            if(index !== -1) {
                allUsers[index] = currentUser;
                DB.saveUsers(allUsers);
            }

            updateProfileUI();
            renderHistory();
        }

        function renderHistory() {
            const grid = document.getElementById('historyGrid');
            grid.innerHTML = '';
            
            if (!currentUser.history || currentUser.history.length === 0) {
                grid.innerHTML = '<p class="text-center text-dim w-100">No swaps yet. Start magic!</p>';
                return;
            }

            currentUser.history.forEach(img => {
                const col = document.createElement('div');
                col.className = 'col-4 col-md-2';
                col.innerHTML = `
                    <div class="history-card">
                        <img src="${img}" onclick="viewHistory('${img}')" style="cursor:pointer">
                    </div>
                `;
                grid.appendChild(col);
            });
        }

        function viewHistory(img) {
            Swal.fire({
                imageUrl: img,
                imageAlt: 'Swap Result',
                showConfirmButton: true,
                confirmButtonText: 'Download',
                showCancelButton: true,
                cancelButtonText: 'Close'
            }).then((result) => {
                if (result.isConfirmed) {
                    const link = document.createElement('a');
                    link.href = img;
                    link.download = 'history_swap.png';
                    link.click();
                }
            });
        }

        function resetSwap() {
            document.getElementById('swapForm').reset();
            document.getElementById('swapForm').style.display = 'block';
            document.getElementById('resultSection').style.display = 'none';
            // Reset previews
            document.getElementById('preview-source').style.display = 'none';
            document.getElementById('info-source').style.display = 'block';
            document.getElementById('btn-rm-source').style.display = 'none';
            document.getElementById('preview-target').style.display = 'none';
            document.getElementById('info-target').style.display = 'block';
            document.getElementById('btn-rm-target').style.display = 'none';
            document.getElementById('submitBtn').disabled = true;
        }

        // Init
        initApp();

    </script>
</body>
</html>
"""

# ==========================================
# FLASK BACKEND
# ==========================================

@app.route("/", methods=["GET"])
def index():
    return render_template_string(html_template)

@app.route("/swap", methods=["POST"])
def face_swap():
    try:
        if "source" not in request.files or "target" not in request.files:
            return jsonify({"success": False, "message": "Missing images"}), 400

        source_img = request.files["source"].read()
        target_img = request.files["target"].read()

        source_b64 = base64.b64encode(source_img).decode()
        target_b64 = base64.b64encode(target_img).decode()

        payload = {
            "source": source_b64,
            "target": target_b64,
            "security": SECURITY_PAYLOAD
        }

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = requests.post(DEEPSWAP_API, json=payload, headers=headers, timeout=120)

        if response.status_code != 200:
            return jsonify({"success": False, "status": response.status_code}), 500

        data = response.json()
        if "result" not in data:
            return jsonify({"success": False, "message": "No result"}), 500

        image_bytes = base64.b64decode(data["result"])

        return send_file(
            io.BytesIO(image_bytes),
            mimetype="image/png",
            as_attachment=False
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)