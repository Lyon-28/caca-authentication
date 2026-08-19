<!DOCTYPE html>
<html lang="id">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
  <title>Caca Auth — Portal</title>
  
  <!-- Font Awesome -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <!-- Google Font -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  
  <style>
    :root {
      --bg-0: #05060a;
      --bg-1: #0b0d14;
      --bg-2: #12141d;
      --surface: #161923;
      --surface-2: #1c202c;
      --border: #262b3a;
      --border-soft: #1e222e;
      --text: #eef0f6;
      --text-dim: #9aa1b5;
      --text-faint: #5c6378;
      --accent: #7c5cff;
      --accent-2: #00e5c7;
      --accent-grad: linear-gradient(135deg, #7c5cff 0%, #00c2ff 50%, #00e5c7 100%);
      --danger: #ff5c7c;
      --warn: #ffb84d;
      --success: #33e2a0;
      --radius: 18px;
      --radius-sm: 12px;
      --shadow-lg: 0 20px 60px -20px rgba(0, 0, 0, 0.6);
      --shadow-glow: 0 0 0 1px rgba(124, 92, 255, 0.15), 0 20px 60px -15px rgba(124, 92, 255, 0.35);
    }
    
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    
    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      background:
        radial-gradient(circle at 15% -10%, rgba(124, 92, 255, 0.18), transparent 40%),
        radial-gradient(circle at 90% 10%, rgba(0, 229, 199, 0.12), transparent 35%),
        var(--bg-0);
      color: var(--text);
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }
    
    ::selection {
      background: var(--accent);
      color: #fff;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
      width: 6px;
    }
    
    ::-webkit-scrollbar-thumb {
      background: var(--border);
      border-radius: 10px;
    }
    
    /* ===== LAYOUT ===== */
    .app-shell {
      max-width: 460px;
      margin: 0 auto;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      position: relative;
    }
    
    /* ===== TOPBAR ===== */
    .topbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 18px 20px;
      position: sticky;
      top: 0;
      z-index: 50;
      background: rgba(5, 6, 10, 0.7);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border-soft);
    }
    
    .brand {
      display: flex;
      align-items: center;
      gap: 10px;
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 700;
      font-size: 17px;
    }
    
    .brand-mark {
      width: 34px;
      height: 34px;
      border-radius: 10px;
      background: var(--accent-grad);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 15px;
      color: #0a0a0f;
      font-weight: 800;
      box-shadow: 0 6px 20px -6px rgba(124, 92, 255, 0.6);
    }
    
    .topbar-actions {
      display: flex;
      gap: 8px;
    }
    
    .icon-btn {
      width: 38px;
      height: 38px;
      border-radius: 12px;
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--text-dim);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: .2s;
      font-size: 14px;
    }
    
    .icon-btn:hover {
      color: var(--text);
      border-color: var(--accent);
      transform: translateY(-1px);
    }
    
    .icon-btn.active {
      color: var(--accent-2);
      border-color: var(--accent-2);
    }
    
    /* ===== MAIN ===== */
    .main {
      flex: 1;
      padding: 24px 20px 100px;
    }
    
    .view {
      display: none;
      animation: fadeUp .35s ease;
    }
    
    .view.active {
      display: block;
    }
    
    @keyframes fadeUp {
      from {
        opacity: 0;
        transform: translateY(10px);
      }
      
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
    
    .view-head {
      margin-bottom: 22px;
    }
    
    .view-eyebrow {
      font-size: 12px;
      letter-spacing: .14em;
      text-transform: uppercase;
      color: var(--accent-2);
      font-weight: 700;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    
    .view-title {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 26px;
      font-weight: 700;
      margin-bottom: 6px;
    }
    
    .view-sub {
      color: var(--text-dim);
      font-size: 14px;
      line-height: 1.5;
    }
    
    /* ===== CARD ===== */
    .card {
      background: linear-gradient(180deg, var(--surface) 0%, var(--bg-1) 100%);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 22px;
      margin-bottom: 16px;
      position: relative;
      overflow: hidden;
    }
    
    .card::before {
      content: "";
      position: absolute;
      inset: 0 0 auto 0;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(124, 92, 255, 0.5), transparent);
    }
    
    .card-title {
      font-weight: 700;
      font-size: 15px;
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    
    .card-title i {
      color: var(--accent-2);
    }
    
    /* ===== FORM ===== */
    .field {
      margin-bottom: 16px;
    }
    
    .field label {
      display: block;
      font-size: 12.5px;
      font-weight: 600;
      color: var(--text-dim);
      margin-bottom: 7px;
      letter-spacing: .02em;
    }
    
    .input-wrap {
      position: relative;
      display: flex;
      align-items: center;
    }
    
    .input-wrap i.fa-icon-left {
      position: absolute;
      left: 14px;
      color: var(--text-faint);
      font-size: 14px;
      pointer-events: none;
    }
    
    input,
    textarea,
    select {
      width: 100%;
      background: var(--bg-1);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 13px 14px;
      border-radius: var(--radius-sm);
      font-size: 14.5px;
      font-family: inherit;
      transition: .2s;
    }
    
    .input-wrap input {
      padding-left: 40px;
    }
    
    .input-wrap.has-toggle input {
      padding-right: 42px;
    }
    
    input:focus,
    textarea:focus,
    select:focus {
      outline: none;
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(124, 92, 255, 0.18);
    }
    
    input::placeholder {
      color: var(--text-faint);
    }
    
    .toggle-eye {
      position: absolute;
      right: 12px;
      background: none;
      border: none;
      color: var(--text-faint);
      cursor: pointer;
      font-size: 14px;
      padding: 6px;
    }
    
    .toggle-eye:hover {
      color: var(--text);
    }
    
    textarea {
      resize: vertical;
      min-height: 80px;
    }
    
    .hint {
      font-size: 12px;
      color: var(--text-faint);
      margin-top: 6px;
    }
    
    .hint.err {
      color: var(--danger);
    }
    
    /* Password strength */
    .strength-bar {
      height: 4px;
      border-radius: 4px;
      background: var(--border);
      margin-top: 8px;
      overflow: hidden;
    }
    
    .strength-fill {
      height: 100%;
      width: 0%;
      transition: .3s;
      border-radius: 4px;
    }
    
    /* ===== BUTTONS ===== */
    .btn {
      width: 100%;
      border: none;
      border-radius: var(--radius-sm);
      padding: 14px 18px;
      font-family: inherit;
      font-weight: 700;
      font-size: 14.5px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: .2s;
      position: relative;
      overflow: hidden;
    }
    
    .btn-primary {
      background: var(--accent-grad);
      color: #0a0a0f;
      box-shadow: 0 10px 30px -10px rgba(124, 92, 255, 0.6);
    }
    
    .btn-primary:hover {
      transform: translateY(-2px);
      box-shadow: 0 14px 34px -10px rgba(124, 92, 255, 0.75);
    }
    
    .btn-primary:active {
      transform: translateY(0);
    }
    
    .btn-outline {
      background: transparent;
      border: 1px solid var(--border);
      color: var(--text);
    }
    
    .btn-outline:hover {
      border-color: var(--accent);
      color: var(--accent-2);
    }
    
    .btn-ghost {
      background: var(--surface-2);
      color: var(--text-dim);
    }
    
    .btn-ghost:hover {
      color: var(--text);
    }
    
    .btn-danger {
      background: rgba(255, 92, 124, 0.12);
      color: var(--danger);
      border: 1px solid rgba(255, 92, 124, 0.3);
    }
    
    .btn-danger:hover {
      background: rgba(255, 92, 124, 0.2);
    }
    
    .btn-sm {
      padding: 9px 14px;
      font-size: 13px;
      width: auto;
    }
    
    .btn[disabled] {
      opacity: .55;
      cursor: not-allowed;
      transform: none !important;
    }
    
    .btn .spinner {
      display: none;
    }
    
    .btn.loading .spinner {
      display: inline-block;
    }
    
    .btn.loading .btn-label {
      opacity: .6;
    }
    
    .spinner {
      width: 16px;
      height: 16px;
      border-radius: 50%;
      border: 2px solid rgba(0, 0, 0, 0.25);
      border-top-color: #0a0a0f;
      animation: spin .7s linear infinite;
    }
    
    .btn-outline .spinner,
    .btn-ghost .spinner {
      border: 2px solid rgba(255, 255, 255, 0.2);
      border-top-color: var(--text);
    }
    
    @keyframes spin {
      to {
        transform: rotate(360deg);
      }
    }
    
    .btn-row {
      display: flex;
      gap: 10px;
    }
    
    .btn-row .btn {
      flex: 1;
    }
    
    .link-row {
      text-align: center;
      margin-top: 16px;
      font-size: 13.5px;
      color: var(--text-dim);
    }
    
    .link-row a {
      color: var(--accent-2);
      text-decoration: none;
      font-weight: 600;
      cursor: pointer;
    }
    
    .link-row a:hover {
      text-decoration: underline;
    }
    
    .divider {
      display: flex;
      align-items: center;
      gap: 12px;
      margin: 18px 0;
      color: var(--text-faint);
      font-size: 12px;
    }
    
    .divider::before,
    .divider::after {
      content: "";
      flex: 1;
      height: 1px;
      background: var(--border);
    }
    
    /* OAuth buttons */
    .oauth-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }
    
    .oauth-btn {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 12px;
      border-radius: var(--radius-sm);
      background: var(--surface-2);
      border: 1px solid var(--border);
      color: var(--text);
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: .2s;
    }
    
    .oauth-btn:hover {
      border-color: var(--accent);
      transform: translateY(-2px);
    }
    
    .oauth-btn.apple {
      grid-column: 1 / -1;
    }
    
    /* Tabs (passwordless) */
    .tabs {
      display: flex;
      gap: 6px;
      background: var(--bg-1);
      padding: 5px;
      border-radius: 12px;
      margin-bottom: 16px;
      border: 1px solid var(--border);
    }
    
    .tab-btn {
      flex: 1;
      border: none;
      background: transparent;
      color: var(--text-faint);
      padding: 9px;
      border-radius: 9px;
      font-size: 12.5px;
      font-weight: 700;
      cursor: pointer;
      transition: .2s;
    }
    
    .tab-btn.active {
      background: var(--accent-grad);
      color: #0a0a0f;
    }
    
    .tab-panel {
      display: none;
    }
    
    .tab-panel.active {
      display: block;
    }
    
    /* OTP boxes */
    .otp-row {
      display: flex;
      gap: 8px;
      justify-content: space-between;
    }
    
    .otp-box {
      width: 44px;
      height: 52px;
      text-align: center;
      font-size: 20px;
      font-weight: 700;
      padding: 0;
      border-radius: 10px;
    }
    
    /* ===== BOTTOM NAV ===== */
    .bottom-nav {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      max-width: 460px;
      margin: 0 auto;
      background: rgba(11, 13, 20, 0.85);
      backdrop-filter: blur(20px);
      border-top: 1px solid var(--border-soft);
      display: flex;
      justify-content: space-around;
      padding: 10px 8px calc(10px + env(safe-area-inset-bottom));
      z-index: 60;
    }
    
    .nav-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
      color: var(--text-faint);
      background: none;
      border: none;
      cursor: pointer;
      font-size: 10.5px;
      font-weight: 600;
      padding: 6px 10px;
      border-radius: 12px;
      transition: .2s;
    }
    
    .nav-item i {
      font-size: 17px;
    }
    
    .nav-item.active {
      color: var(--accent-2);
    }
    
    .nav-item.active i {
      transform: translateY(-1px);
    }
    
    /* ===== PROFILE ===== */
    .profile-hero {
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      padding: 10px 0 22px;
    }
    
    .avatar-wrap {
      position: relative;
      width: 96px;
      height: 96px;
      margin-bottom: 14px;
    }
    
    .avatar-img {
      width: 96px;
      height: 96px;
      border-radius: 50%;
      object-fit: cover;
      background: var(--accent-grad);
      border: 3px solid var(--surface);
      box-shadow: 0 8px 26px -8px rgba(124, 92, 255, 0.6);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 34px;
      font-weight: 800;
      color: #0a0a0f;
    }
    
    .avatar-edit {
      position: absolute;
      bottom: 0;
      right: 0;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: var(--accent);
      border: 3px solid var(--bg-0);
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 12px;
    }
    
    .profile-name {
      font-family: 'Space Grotesk';
      font-size: 20px;
      font-weight: 700;
    }
    
    .profile-email {
      color: var(--text-dim);
      font-size: 13px;
      margin-top: 2px;
    }
    
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      margin-top: 10px;
      padding: 5px 12px;
      border-radius: 20px;
      font-size: 11.5px;
      font-weight: 700;
      background: rgba(51, 226, 160, 0.12);
      color: var(--success);
      border: 1px solid rgba(51, 226, 160, 0.3);
    }
    
    .badge.warn {
      background: rgba(255, 184, 77, 0.12);
      color: var(--warn);
      border-color: rgba(255, 184, 77, 0.3);
    }
    
    .stat-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-bottom: 16px;
    }
    
    .stat-box {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 14px;
      text-align: center;
    }
    
    .stat-box .num {
      font-family: 'Space Grotesk';
      font-size: 20px;
      font-weight: 700;
      color: var(--accent-2);
    }
    
    .stat-box .lbl {
      font-size: 11px;
      color: var(--text-faint);
      margin-top: 2px;
    }
    
    .list-item {
      display: flex;
      align-items: center;
      justify-content: between;
      gap: 12px;
      padding: 14px;
      border-radius: 14px;
      border: 1px solid var(--border-soft);
      background: var(--bg-1);
      margin-bottom: 10px;
      cursor: pointer;
      transition: .2s;
    }
    
    .list-item:hover {
      border-color: var(--accent);
    }
    
    .list-item .li-icon {
      width: 38px;
      height: 38px;
      border-radius: 10px;
      background: var(--surface-2);
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--accent-2);
      flex-shrink: 0;
    }
    
    .list-item .li-body {
      flex: 1;
    }
    
    .list-item .li-title {
      font-size: 13.5px;
      font-weight: 600;
    }
    
    .list-item .li-sub {
      font-size: 11.5px;
      color: var(--text-faint);
      margin-top: 1px;
    }
    
    .list-item .li-arrow {
      color: var(--text-faint);
      font-size: 12px;
    }
    
    /* Toggle switch */
    .switch {
      position: relative;
      width: 44px;
      height: 25px;
      flex-shrink: 0;
    }
    
    .switch input {
      opacity: 0;
      width: 0;
      height: 0;
    }
    
    .slider-toggle {
      position: absolute;
      inset: 0;
      background: var(--border);
      border-radius: 20px;
      cursor: pointer;
      transition: .3s;
    }
    
    .slider-toggle::before {
      content: "";
      position: absolute;
      width: 19px;
      height: 19px;
      left: 3px;
      top: 3px;
      background: #fff;
      border-radius: 50%;
      transition: .3s;
    }
    
    input:checked+.slider-toggle {
      background: var(--accent-grad);
    }
    
    input:checked+.slider-toggle::before {
      transform: translateX(19px);
    }
    
    /* Session item */
    .session-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 14px;
      border: 1px solid var(--border-soft);
      border-radius: 14px;
      margin-bottom: 10px;
      background: var(--bg-1);
    }
    
    .session-icon {
      width: 36px;
      height: 36px;
      border-radius: 10px;
      background: var(--surface-2);
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--accent-2);
    }
    
    .session-body {
      flex: 1;
    }
    
    .session-device {
      font-size: 13.5px;
      font-weight: 600;
    }
    
    .session-meta {
      font-size: 11.5px;
      color: var(--text-faint);
      margin-top: 2px;
    }
    
    .session-current {
      font-size: 10px;
      color: var(--success);
      font-weight: 700;
    }
    
    .session-revoke {
      background: none;
      border: none;
      color: var(--danger);
      cursor: pointer;
      font-size: 15px;
      padding: 6px;
    }
    
    /* MFA */
    .qr-box {
      display: flex;
      align-items: center;
      justify-content: center;
      background: #fff;
      border-radius: 14px;
      padding: 16px;
      margin-bottom: 14px;
    }
    
    .qr-box img {
      width: 100%;
      max-width: 200px;
    }
    
    .secret-box {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      background: var(--bg-1);
      border: 1px dashed var(--border);
      border-radius: 12px;
      padding: 12px 14px;
      font-family: monospace;
      font-size: 13px;
      letter-spacing: .05em;
      word-break: break-all;
      margin-bottom: 16px;
    }
    
    .copy-btn {
      background: none;
      border: none;
      color: var(--accent-2);
      cursor: pointer;
      font-size: 14px;
      flex-shrink: 0;
    }
    
    /* Empty state */
    .empty-state {
      text-align: center;
      padding: 40px 20px;
      color: var(--text-faint);
    }
    
    .empty-state i {
      font-size: 34px;
      margin-bottom: 12px;
      opacity: .5;
    }
    
    .empty-state p {
      font-size: 13px;
    }
    
    /* ===== TOAST / ALERT ===== */
    .toast-stack {
      position: fixed;
      top: 16px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 999;
      display: flex;
      flex-direction: column;
      gap: 10px;
      width: calc(100% - 32px);
      max-width: 420px;
      pointer-events: none;
    }
    
    .toast {
      pointer-events: auto;
      display: flex;
      align-items: flex-start;
      gap: 11px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 13px 14px;
      box-shadow: var(--shadow-lg);
      animation: toastIn .35s cubic-bezier(.2, .9, .3, 1.3);
      backdrop-filter: blur(10px);
    }
    
    .toast.hide {
      animation: toastOut .3s ease forwards;
    }
    
    @keyframes toastIn {
      from {
        opacity: 0;
        transform: translateY(-16px) scale(.95);
      }
      
      to {
        opacity: 1;
        transform: translateY(0) scale(1);
      }
    }
    
    @keyframes toastOut {
      to {
        opacity: 0;
        transform: translateY(-10px) scale(.95);
      }
    }
    
    .toast-icon {
      width: 30px;
      height: 30px;
      border-radius: 9px;
      flex-shrink: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 13px;
    }
    
    .toast.success .toast-icon {
      background: rgba(51, 226, 160, 0.15);
      color: var(--success);
    }
    
    .toast.error .toast-icon {
      background: rgba(255, 92, 124, 0.15);
      color: var(--danger);
    }
    
    .toast.warn .toast-icon {
      background: rgba(255, 184, 77, 0.15);
      color: var(--warn);
    }
    
    .toast.info .toast-icon {
      background: rgba(0, 194, 255, 0.15);
      color: #00c2ff;
    }
    
    .toast-content {
      flex: 1;
    }
    
    .toast-title {
      font-size: 13.5px;
      font-weight: 700;
      margin-bottom: 2px;
    }
    
    .toast-msg {
      font-size: 12.5px;
      color: var(--text-dim);
      line-height: 1.4;
    }
    
    .toast-close {
      background: none;
      border: none;
      color: var(--text-faint);
      cursor: pointer;
      font-size: 12px;
      padding: 2px;
    }
    
    /* ===== CONFIRM MODAL ===== */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(5, 6, 10, 0.75);
      backdrop-filter: blur(6px);
      display: none;
      align-items: flex-end;
      justify-content: center;
      z-index: 200;
    }
    
    .modal-overlay.show {
      display: flex;
      animation: fadeIn .2s ease;
    }
    
    @keyframes fadeIn {
      from {
        opacity: 0;
      }
      
      to {
        opacity: 1;
      }
    }
    
    .modal-sheet {
      width: 100%;
      max-width: 460px;
      background: var(--bg-1);
      border: 1px solid var(--border);
      border-bottom: none;
      border-radius: 22px 22px 0 0;
      padding: 22px 20px calc(22px + env(safe-area-inset-bottom));
      animation: sheetUp .3s cubic-bezier(.2, .9, .3, 1.1);
    }
    
    @keyframes sheetUp {
      from {
        transform: translateY(100%);
      }
      
      to {
        transform: translateY(0);
      }
    }
    
    .modal-handle {
      width: 40px;
      height: 4px;
      background: var(--border);
      border-radius: 4px;
      margin: 0 auto 18px;
    }
    
    .modal-icon {
      width: 52px;
      height: 52px;
      border-radius: 50%;
      margin: 0 auto 14px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      background: rgba(255, 92, 124, 0.12);
      color: var(--danger);
    }
    
    .modal-title {
      text-align: center;
      font-weight: 700;
      font-size: 17px;
      margin-bottom: 6px;
    }
    
    .modal-text {
      text-align: center;
      color: var(--text-dim);
      font-size: 13.5px;
      line-height: 1.5;
      margin-bottom: 20px;
    }
    
    /* Loading overlay for full-screen actions */
    .page-loader {
      position: fixed;
      inset: 0;
      background: rgba(5, 6, 10, 0.6);
      backdrop-filter: blur(4px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 300;
    }
    
    .page-loader.show {
      display: flex;
    }
    
    .page-loader .ring {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      border: 3px solid rgba(124, 92, 255, 0.2);
      border-top-color: var(--accent);
      animation: spin .8s linear infinite;
    }
    
    input.input-error,
    textarea.input-error {
      border-color: var(--danger) !important;
      box-shadow: 0 0 0 3px rgba(255, 92, 124, 0.15) !important;
    }
    
    .skeleton {
      background: linear-gradient(90deg, var(--surface) 25%, var(--surface-2) 50%, var(--surface) 75%);
      background-size: 200% 100%;
      animation: shimmer 1.5s infinite;
      border-radius: 8px;
    }
    
    @keyframes shimmer {
      0% {
        background-position: 200% 0;
      }
      
      100% {
        background-position: -200% 0;
      }
    }
    
    /* Utility */
    .mt-8 {
      margin-top: 8px;
    }
    
    .mt-16 {
      margin-top: 16px;
    }
    
    .mb-0 {
      margin-bottom: 0;
    }
    
    .text-center {
      text-align: center;
    }
    
    .small-note {
      font-size: 12px;
      color: var(--text-faint);
      line-height: 1.5;
    }
    
    @media (min-width:480px) {
      .app-shell {
        padding-top: 0;
      }
    }
  </style>
</head>

<body>
  
  <div class="app-shell">
    
    <!-- ===== TOPBAR ===== -->
    <div class="topbar" id="topbar">
      <div class="brand">
        <div class="brand-mark">C</div>
        <span>Caca Auth</span>
      </div>
      <div class="topbar-actions" id="topbarActions">
        <!-- diisi dinamis via JS sesuai status login -->
      </div>
    </div>
    
    <!-- ===== MAIN ===== -->
    <div class="main">
      
      <!-- ========== VIEW: LOGIN ========== -->
      <section class="view active" id="view-login">
        <div class="view-head">
          <div class="view-eyebrow"><i class="fa-solid fa-shield-halved"></i> Secure Access</div>
          <div class="view-title">Selamat datang kembali</div>
          <div class="view-sub">Masuk untuk melanjutkan ke akunmu.</div>
        </div>
        
        <div class="card">
          <form id="formLogin">
            <div class="field">
              <label>Email</label>
              <div class="input-wrap">
                <i class="fa-solid fa-envelope fa-icon-left"></i>
                <input type="email" id="loginEmail" placeholder="nama@email.com" required>
              </div>
            </div>
            <div class="field mb-0">
              <label>Password</label>
              <div class="input-wrap has-toggle">
                <i class="fa-solid fa-lock fa-icon-left"></i>
                <input type="password" id="loginPassword" placeholder="••••••••" required>
                <button type="button" class="toggle-eye" data-toggle="loginPassword"><i class="fa-solid fa-eye"></i></button>
              </div>
            </div>
            <div class="text-center mt-8">
              <a onclick="showView('forgot')" style="font-size:12.5px;color:var(--accent-2);cursor:pointer;">Lupa password?</a>
            </div>
            
            <button type="submit" class="btn btn-primary mt-16">
              <span class="spinner"></span>
              <i class="fa-solid fa-arrow-right-to-bracket btn-label"></i>
              <span class="btn-label">Masuk</span>
            </button>
          </form>
          
          <div class="divider">atau lanjutkan tanpa password</div>
          <button class="btn btn-outline" onclick="showView('passwordless')">
            <i class="fa-solid fa-wand-magic-sparkles"></i> Login Tanpa Password
          </button>
          
          <div class="divider">atau via</div>
          <div class="oauth-grid">
            <button class="oauth-btn" onclick="oauthStart('google')"><i class="fa-brands fa-google"></i> Google</button>
            <button class="oauth-btn" onclick="oauthStart('github')"><i class="fa-brands fa-github"></i> GitHub</button>
            <button class="oauth-btn apple" onclick="oauthStart('apple')"><i class="fa-brands fa-apple"></i> Lanjut dengan Apple</button>
          </div>
        </div>
        
        <div class="link-row">Belum punya akun? <a onclick="showView('register')">Daftar sekarang</a></div>
      </section>
      
      <!-- ========== VIEW: REGISTER ========== -->
      <section class="view" id="view-register">
        <div class="view-head">
          <div class="view-eyebrow"><i class="fa-solid fa-user-plus"></i> Bergabung</div>
          <div class="view-title">Buat akun baru</div>
          <div class="view-sub">Cepat, aman, dan gratis.</div>
        </div>
        
        <div class="card">
          <form id="formRegister">
            <div class="field">
              <label>Email</label>
              <div class="input-wrap">
                <i class="fa-solid fa-envelope fa-icon-left"></i>
                <input type="email" id="regEmail" placeholder="nama@email.com" required>
              </div>
            </div>
            <div class="field">
              <label>Password</label>
              <div class="input-wrap has-toggle">
                <i class="fa-solid fa-lock fa-icon-left"></i>
                <input type="password" id="regPassword" placeholder="Minimal 8 karakter" required oninput="checkStrength(this.value)">
                <button type="button" class="toggle-eye" data-toggle="regPassword"><i class="fa-solid fa-eye"></i></button>
              </div>
              <div class="strength-bar">
                <div class="strength-fill" id="strengthFill"></div>
              </div>
              <div class="hint" id="strengthLabel">Kekuatan password</div>
            </div>
            <button type="submit" class="btn btn-primary mt-16">
              <span class="spinner"></span>
              <i class="fa-solid fa-user-plus btn-label"></i>
              <span class="btn-label">Daftar</span>
            </button>
          </form>
        </div>
        
        <div class="link-row">Sudah punya akun? <a onclick="showView('login')">Masuk di sini</a></div>
      </section>
      
      <!-- ========== VIEW: PASSWORDLESS ========== -->
      <section class="view" id="view-passwordless">
        <div class="view-head">
          <button class="icon-btn mb-0" onclick="showView('login')" style="margin-bottom:14px;"><i class="fa-solid fa-arrow-left"></i></button>
          <div class="view-eyebrow"><i class="fa-solid fa-wand-magic-sparkles"></i> Passwordless</div>
          <div class="view-title">Login tanpa password</div>
          <div class="view-sub">Pilih metode yang kamu suka.</div>
        </div>
        
        <div class="card">
          <div class="tabs">
            <button class="tab-btn active" data-tab="magic" onclick="switchTab('magic')">Magic Link</button>
            <button class="tab-btn" data-tab="otp" onclick="switchTab('otp')">OTP SMS</button>
            <button class="tab-btn" data-tab="anon" onclick="switchTab('anon')">Tamu</button>
          </div>
          
          <!-- Magic Link -->
          <div class="tab-panel active" id="tab-magic">
            <form id="formMagicRequest">
              <div class="field mb-0">
                <label>Email</label>
                <div class="input-wrap">
                  <i class="fa-solid fa-envelope fa-icon-left"></i>
                  <input type="email" id="magicEmail" placeholder="nama@email.com" required>
                </div>
              </div>
              <button type="submit" class="btn btn-primary mt-16">
                <span class="spinner"></span>
                <i class="fa-solid fa-paper-plane btn-label"></i>
                <span class="btn-label">Kirim Magic Link</span>
              </button>
            </form>
            <p class="small-note mt-8">Kami akan mengirim tautan login sekali-pakai ke email kamu.</p>
          </div>
          
          <!-- OTP -->
          <div class="tab-panel" id="tab-otp">
            <form id="formOtpRequest">
              <div class="field mb-0">
                <label>Nomor HP</label>
                <div class="input-wrap">
                  <i class="fa-solid fa-phone fa-icon-left"></i>
                  <input type="tel" id="otpPhone" placeholder="+62 812xxxxxxx" required>
                </div>
              </div>
              <button type="submit" class="btn btn-primary mt-16">
                <span class="spinner"></span>
                <i class="fa-solid fa-comment-sms btn-label"></i>
                <span class="btn-label">Kirim Kode OTP</span>
              </button>
            </form>
            
            <form id="formOtpVerify" style="display:none;" class="mt-16">
              <label style="font-size:12.5px;font-weight:600;color:var(--text-dim);margin-bottom:10px;display:block;">Masukkan 6 digit kode</label>
              <div class="otp-row">
                <input class="otp-box" maxlength="1" inputmode="numeric">
                <input class="otp-box" maxlength="1" inputmode="numeric">
                <input class="otp-box" maxlength="1" inputmode="numeric">
                <input class="otp-box" maxlength="1" inputmode="numeric">
                <input class="otp-box" maxlength="1" inputmode="numeric">
                <input class="otp-box" maxlength="1" inputmode="numeric">
              </div>
              <button type="submit" class="btn btn-primary mt-16">
                <span class="spinner"></span>
                <i class="fa-solid fa-check btn-label"></i>
                <span class="btn-label">Verifikasi</span>
              </button>
            </form>
          </div>
          
          <!-- Anonymous -->
          <div class="tab-panel" id="tab-anon">
            <p class="small-note mt-8" style="margin-bottom:16px;">Masuk sebagai tamu tanpa mendaftar. Beberapa fitur mungkin terbatas.</p>
            <button class="btn btn-primary" onclick="loginAnonymous()" id="btnAnon">
              <span class="spinner"></span>
              <i class="fa-solid fa-user-secret btn-label"></i>
              <span class="btn-label">Lanjutkan sebagai Tamu</span>
            </button>
          </div>
        </div>
      </section>
      
      <!-- ========== VIEW: FORGOT PASSWORD ========== -->
      <section class="view" id="view-forgot">
        <div class="view-head">
          <button class="icon-btn mb-0" onclick="showView('login')" style="margin-bottom:14px;"><i class="fa-solid fa-arrow-left"></i></button>
          <div class="view-eyebrow"><i class="fa-solid fa-key"></i> Pemulihan</div>
          <div class="view-title">Lupa password?</div>
          <div class="view-sub">Masukkan email untuk menerima tautan reset.</div>
        </div>
        
        <div class="card">
          <form id="formForgot">
            <div class="field mb-0">
              <label>Email</label>
              <div class="input-wrap">
                <i class="fa-solid fa-envelope fa-icon-left"></i>
                <input type="email" id="forgotEmail" placeholder="nama@email.com" required>
              </div>
            </div>
            <button type="submit" class="btn btn-primary mt-16">
              <span class="spinner"></span>
              <i class="fa-solid fa-paper-plane btn-label"></i>
              <span class="btn-label">Kirim Tautan Reset</span>
            </button>
          </form>
        </div>
        
        <div class="card">
          <div class="card-title"><i class="fa-solid fa-rotate"></i> Sudah punya token reset?</div>
          <form id="formReset">
            <div class="field">
              <label>Token</label>
              <div class="input-wrap">
                <i class="fa-solid fa-ticket fa-icon-left"></i>
                <input type="text" id="resetToken" placeholder="Token dari email" required>
              </div>
            </div>
            <div class="field mb-0">
              <label>Password Baru</label>
              <div class="input-wrap has-toggle">
                <i class="fa-solid fa-lock fa-icon-left"></i>
                <input type="password" id="resetNewPassword" placeholder="Password baru" required>
                <button type="button" class="toggle-eye" data-toggle="resetNewPassword"><i class="fa-solid fa-eye"></i></button>
              </div>
            </div>
            <button type="submit" class="btn btn-outline mt-16">
              <span class="spinner"></span>
              <i class="fa-solid fa-check btn-label"></i>
              <span class="btn-label">Reset Password</span>
            </button>
          </form>
        </div>
      </section>
      
      <!-- ========== VIEW: VERIFY EMAIL ========== -->
      <section class="view" id="view-verify">
        <div class="view-head">
          <div class="view-eyebrow"><i class="fa-solid fa-envelope-circle-check"></i> Verifikasi</div>
          <div class="view-title">Verifikasi email kamu</div>
          <div class="view-sub">Masukkan token yang dikirim ke email, atau minta ulang.</div>
        </div>
        <div class="card">
          <form id="formVerifyEmail">
            <div class="field mb-0">
              <label>Token Verifikasi</label>
              <div class="input-wrap">
                <i class="fa-solid fa-ticket fa-icon-left"></i>
                <input type="text" id="verifyToken" placeholder="Token dari email" required>
              </div>
            </div>
            <button type="submit" class="btn btn-primary mt-16">
              <span class="spinner"></span>
              <i class="fa-solid fa-check-double btn-label"></i>
              <span class="btn-label">Verifikasi Email</span>
            </button>
          </form>
          <button class="btn btn-ghost mt-8" onclick="resendVerification()" id="btnResend">
            <span class="spinner"></span>
            <i class="fa-solid fa-rotate btn-label"></i>
            <span class="btn-label">Kirim Ulang Email Verifikasi</span>
          </button>
        </div>
      </section>
      
      <!-- ========== VIEW: HOME / DASHBOARD ========== -->
      <section class="view" id="view-home">
        <div class="view-head">
          <div class="view-eyebrow"><i class="fa-solid fa-house"></i> Beranda</div>
          <div class="view-title" id="homeGreeting">Halo 👋</div>
          <div class="view-sub">Semua sistemmu terpantau di sini.</div>
        </div>
        
        <div class="stat-grid">
          <div class="stat-box">
            <div class="num" id="statSessions">-</div>
            <div class="lbl">Sesi Aktif</div>
          </div>
          <div class="stat-box">
            <div class="num" id="statMfa">-</div>
            <div class="lbl">Status MFA</div>
          </div>
        </div>
        
        <div class="card">
          <div class="card-title"><i class="fa-solid fa-bolt"></i> Aksi Cepat</div>
          <div class="list-item" onclick="showView('profile')">
            <div class="li-icon"><i class="fa-solid fa-id-card"></i></div>
            <div class="li-body">
              <div class="li-title">Kelola Profil</div>
              <div class="li-sub">Nama, bio, avatar</div>
            </div>
            <i class="fa-solid fa-chevron-right li-arrow"></i>
          </div>
          <div class="list-item" onclick="showView('security')">
            <div class="li-icon"><i class="fa-solid fa-shield-halved"></i></div>
            <div class="li-body">
              <div class="li-title">Keamanan & MFA</div>
              <div class="li-sub">2FA, sesi, password</div>
            </div>
            <i class="fa-solid fa-chevron-right li-arrow"></i>
          </div>
          <div class="list-item mb-0" onclick="showView('terms')">
            <div class="li-icon"><i class="fa-solid fa-file-contract"></i></div>
            <div class="li-body">
              <div class="li-title">Syarat & Ketentuan</div>
              <div class="li-sub">Status persetujuan</div>
            </div>
            <i class="fa-solid fa-chevron-right li-arrow"></i>
          </div>
        </div>
      </section>
      
      <!-- ========== VIEW: PROFILE ========== -->
      <section class="view" id="view-profile">
        <div class="view-head">
          <div class="view-eyebrow"><i class="fa-solid fa-id-card"></i> Akun</div>
          <div class="view-title">Profil Saya</div>
        </div>
        
        <div class="profile-hero">
          <div class="avatar-wrap">
            <div class="avatar-img" id="avatarPreview">?</div>
            <div class="avatar-edit" onclick="document.getElementById('avatarInput').click()"><i class="fa-solid fa-camera"></i></div>
            <input type="file" id="avatarInput" accept="image/*" style="display:none;" onchange="uploadAvatar(this.files[0])">
          </div>
          <button class="btn btn-ghost btn-sm mt-8" onclick="confirmAction('deleteAvatar')" id="btnDeleteAvatar" style="display:none;">
            <i class="fa-solid fa-trash"></i> Hapus Foto Profil
          </button>
          <div class="profile-name" id="profileName">Pengguna</div>
          <div class="profile-email" id="profileEmail">-</div>
          <div class="badge" id="verifyBadge"><i class="fa-solid fa-circle-check"></i> Terverifikasi</div>
        </div>
        
        <div class="card">
          <div class="card-title"><i class="fa-solid fa-pen"></i> Edit Profil</div>
          <form id="formProfile">
            <div class="field">
              <label>Nama</label>
              <div class="input-wrap">
                <i class="fa-solid fa-user fa-icon-left"></i>
                <input type="text" id="profileNameInput" placeholder="Nama lengkap">
              </div>
            </div>
            <div class="field">
              <label>Bio</label>
              <textarea id="profileBioInput" placeholder="Ceritakan tentang dirimu..."></textarea>
            </div>
            <div class="field mb-0">
              <label>Tanggal Lahir</label>
              <div class="input-wrap">
                <i class="fa-solid fa-cake-candles fa-icon-left"></i>
                <input type="date" id="profileBirthInput">
              </div>
            </div>
            <button type="submit" class="btn btn-primary mt-16">
              <span class="spinner"></span>
              <i class="fa-solid fa-floppy-disk btn-label"></i>
              <span class="btn-label">Simpan Perubahan</span>
            </button>
          </form>
        </div>
        
        <div class="card">
          <div class="card-title"><i class="fa-solid fa-envelope"></i> Ubah Email</div>
          <form id="formChangeEmail">
            <div class="field mb-0">
              <label>Email Baru</label>
              <div class="input-wrap">
                <i class="fa-solid fa-envelope fa-icon-left"></i>
                <input type="email" id="newEmailInput" placeholder="email-baru@mail.com" required>
              </div>
            </div>
            <button type="submit" class="btn btn-outline mt-16">
              <span class="spinner"></span>
              <i class="fa-solid fa-paper-plane btn-label"></i>
              <span class="btn-label">Kirim Konfirmasi</span>
            </button>
          </form>
        </div>
        
        <div class="card">
          <div class="card-title"><i class="fa-solid fa-file-arrow-up"></i> Unggah Dokumen</div>
          <p class="small-note" style="margin-bottom:14px;">Unggah dokumen pendukung (KTP, sertifikat, dll).</p>
          <input type="file" id="documentInput" style="display:none;" onchange="uploadDocument(this.files[0])">
          <button class="btn btn-outline" onclick="document.getElementById('documentInput').click()" id="btnUploadDoc">
            <span class="spinner"></span>
            <i class="fa-solid fa-upload btn-label"></i>
            <span class="btn-label">Pilih & Unggah File</span>
          </button>
          <div id="uploadedDocInfo" class="hint mt-8"></div>
        </div>
        
        <div class="card">
          <div class="card-title"><i class="fa-solid fa-sliders"></i> Preferensi</div>
          <div class="field">
            <label>Bahasa</label>
            <select id="prefLanguage">
              <option value="id">Indonesia</option>
              <option value="en">English</option>
            </select>
          </div>
          <div class="field">
            <label>Zona Waktu</label>
            <select id="prefTimezone">
              <option value="Asia/Jakarta">WIB (Jakarta)</option>
              <option value="Asia/Makassar">WITA (Makassar)</option>
              <option value="Asia/Jayapura">WIT (Jayapura)</option>
            </select>
          </div>
          <div class="list-item" style="cursor:default;">
            <div class="li-icon"><i class="fa-solid fa-bell"></i></div>
            <div class="li-body">
              <div class="li-title">Notifikasi</div>
              <div class="li-sub">Terima update via email</div>
            </div>
            <label class="switch"><input type="checkbox" id="prefNotif" checked><span class="slider-toggle"></span></label>
          </div>
          <div class="list-item mb-0" style="cursor:default;">
            <div class="li-icon"><i class="fa-solid fa-eye"></i></div>
            <div class="li-body">
              <div class="li-title">Profil Publik</div>
              <div class="li-sub">Terlihat oleh pengguna lain</div>
            </div>
            <label class="switch"><input type="checkbox" id="prefPublic"><span class="slider-toggle"></span></label>
          </div>
          <button class="btn btn-primary mt-16" onclick="savePreferences()" id="btnSavePref">
            <span class="spinner"></span>
            <i class="fa-solid fa-check btn-label"></i>
            <span class="btn-label">Simpan Preferensi</span>
          </button>
        </div>
        
        <div class="card">
          <div class="card-title" style="color:var(--danger);"><i class="fa-solid fa-triangle-exclamation"></i> Zona Berbahaya</div>
          <div class="btn-row">
            <button class="btn btn-ghost" onclick="confirmAction('deactivate')">
              <i class="fa-solid fa-pause"></i> Nonaktifkan
            </button>
            <button class="btn btn-danger" onclick="showDeleteOptions()">
              <i class="fa-solid fa-trash"></i> Hapus Akun
            </button>
          </div>
        </div>
      </section>
      
      <!-- ========== VIEW: SECURITY (password, MFA, sessions) ========== -->
      <section class="view" id="view-security">
        <div class="view-head">
          <div class="view-eyebrow"><i class="fa-solid fa-shield-halved"></i> Keamanan</div>
          <div class="view-title">Keamanan Akun</div>
        </div>
        
        <div class="card">
          <div class="card-title"><i class="fa-solid fa-key"></i> Ubah Password</div>
          <form id="formChangePassword">
            <div class="field">
              <label>Password Lama</label>
              <div class="input-wrap has-toggle">
                <i class="fa-solid fa-lock fa-icon-left"></i>
                <input type="password" id="oldPassword" placeholder="Password saat ini" required>
                <button type="button" class="toggle-eye" data-toggle="oldPassword"><i class="fa-solid fa-eye"></i></button>
              </div>
            </div>
            <div class="field mb-0">
              <label>Password Baru</label>
              <div class="input-wrap has-toggle">
                <i class="fa-solid fa-lock fa-icon-left"></i>
                <input type="password" id="newPassword" placeholder="Password baru" required>
                <button type="button" class="toggle-eye" data-toggle="newPassword"><i class="fa-solid fa-eye"></i></button>
              </div>
            </div>
            <button type="submit" class="btn btn-primary mt-16">
              <span class="spinner"></span>
              <i class="fa-solid fa-check btn-label"></i>
              <span class="btn-label">Perbarui Password</span>
            </button>
          </form>
        </div>
        
        <div class="card">
          <div class="card-title"><i class="fa-solid fa-mobile-screen-button"></i> Autentikasi Dua Faktor (TOTP)</div>
          <div id="mfaNotSetup">
            <p class="small-note mt-8" style="margin-bottom:14px;">Amankan akunmu dengan Google Authenticator / Authy.</p>
            <button class="btn btn-primary" onclick="setupTotp()" id="btnSetupTotp">
              <span class="spinner"></span>
              <i class="fa-solid fa-qrcode btn-label"></i>
              <span class="btn-label">Aktifkan MFA</span>
            </button>
          </div>
          <div id="mfaSetupPanel" style="display:none;">
            <div class="qr-box"><img id="totpQr" src="" alt="QR Code"></div>
            <div class="secret-box">
              <span id="totpSecret">-</span>
              <button class="copy-btn" onclick="copySecret()"><i class="fa-regular fa-copy"></i></button>
            </div>
            <form id="formEnableTotp">
              <div class="field mb-0">
                <label>Kode dari Authenticator</label>
                <div class="input-wrap">
                  <i class="fa-solid fa-shield-halved fa-icon-left"></i>
                  <input type="text" id="totpEnableCode" placeholder="123456" maxlength="6" required>
                </div>
              </div>
              <button type="submit" class="btn btn-primary mt-16">
                <span class="spinner"></span>
                <i class="fa-solid fa-check btn-label"></i>
                <span class="btn-label">Konfirmasi & Aktifkan</span>
              </button>
            </form>
          </div>
          <div id="mfaActivePanel" style="display:none;">
            <div class="badge mt-8" style="margin-bottom:14px;"><i class="fa-solid fa-shield-halved"></i> MFA Aktif</div>
            <form id="formDisableTotp">
              <div class="field mb-0">
                <label>Masukkan kode untuk menonaktifkan</label>
                <div class="input-wrap">
                  <i class="fa-solid fa-shield-halved fa-icon-left"></i>
                  <input type="text" id="totpDisableCode" placeholder="123456" maxlength="6" required>
                </div>
              </div>
              <button type="submit" class="btn btn-danger mt-16">
                <span class="spinner"></span>
                <i class="fa-solid fa-xmark btn-label"></i>
                <span class="btn-label">Nonaktifkan MFA</span>
              </button>
            </form>
          </div>
        </div>
        
        <div class="card">
          <div class="card-title"><i class="fa-solid fa-desktop"></i> Sesi Aktif</div>
          <div id="sessionList">
            <div class="empty-state"><i class="fa-solid fa-spinner fa-spin"></i>
              <p>Memuat sesi...</p>
            </div>
          </div>
          <button class="btn btn-danger mt-8" onclick="confirmAction('logoutAll')">
            <i class="fa-solid fa-power-off"></i> Keluar dari Semua Perangkat
          </button>
        </div>
      </section>
      
      <!-- ========== VIEW: TERMS ========== -->
      <section class="view" id="view-terms">
        <div class="view-head">
          <div class="view-eyebrow"><i class="fa-solid fa-file-contract"></i> Legal</div>
          <div class="view-title">Syarat & Ketentuan</div>
        </div>
        <div class="card">
          <div class="card-title"><i class="fa-solid fa-circle-info"></i> Status Persetujuan</div>
          <div id="termsStatusBox" class="small-note">Memuat status...</div>
        </div>
        <div class="card">
          <div class="card-title"><i class="fa-solid fa-scroll"></i> Versi Terbaru</div>
          <div id="termsContentBox" class="small-note" style="max-height:220px; overflow-y:auto; margin-bottom:16px;">Memuat konten...</div>
          <button class="btn btn-primary" onclick="acceptTerms()" id="btnAcceptTerms">
            <span class="spinner"></span>
            <i class="fa-solid fa-check btn-label"></i>
            <span class="btn-label">Saya Setuju</span>
          </button>
        </div>
      </section>
      
    </div>
    
    <!-- ===== BOTTOM NAV (muncul saat login) ===== -->
    <div class="bottom-nav" id="bottomNav" style="display:none;">
      <button class="nav-item active" data-nav="home" onclick="showView('home')"><i class="fa-solid fa-house"></i>Beranda</button>
      <button class="nav-item" data-nav="profile" onclick="showView('profile')"><i class="fa-solid fa-id-card"></i>Profil</button>
      <button class="nav-item" data-nav="security" onclick="showView('security')"><i class="fa-solid fa-shield-halved"></i>Keamanan</button>
      <button class="nav-item" data-nav="terms" onclick="showView('terms')"><i class="fa-solid fa-file-contract"></i>Terms</button>
    </div>
    
  </div>
  
  <!-- ===== TOAST STACK ===== -->
  <div class="toast-stack" id="toastStack"></div>
  
  <!-- ===== CONFIRM MODAL ===== -->
  <div class="modal-overlay" id="modalOverlay">
    <div class="modal-sheet">
      <div class="modal-handle"></div>
      <div class="modal-icon" id="modalIcon"><i class="fa-solid fa-triangle-exclamation"></i></div>
      <div class="modal-title" id="modalTitle">Konfirmasi</div>
      <div class="modal-text" id="modalText">Apakah kamu yakin?</div>
      <div class="btn-row">
        <button class="btn btn-ghost" onclick="closeModal()">Batal</button>
        <button class="btn btn-danger" id="modalConfirmBtn">Ya, Lanjutkan</button>
      </div>
    </div>
  </div>
  
  <!-- ===== PAGE LOADER ===== -->
  <div class="page-loader" id="pageLoader">
    <div class="ring"></div>
  </div>
  
  <script>
    /* =========================================================
   CACA AUTH — FRONTEND CLIENT
   Mencakup semua endpoint API
========================================================= */
    
    const BASE = "https://caca-authentication.vercel.app";
    const API_KEY = "caca-pk_cv1wxlGUrc36asVvIPC_r3AjHxoEzlICdtln0oHQnPE"; // ganti dengan API key tenant kamu
    
    let state = {
      accessToken: localStorage.getItem("caca_access_token") || null,
      refreshToken: localStorage.getItem("caca_refresh_token") || null,
      user: null,
      pendingOtpPhone: null,
      pendingEmail: null, // BARU
      totpSecret: null
    };
    
    /* ---------- Core fetch wrapper ---------- */
    let isRefreshing = false;
    
    async function apiCall(path, { method = "GET", body, auth = false, useApiKey = false, isForm = false, query, _retry = false } = {}) {
      const headers = {};
      if (!isForm) headers["Content-Type"] = "application/json";
      if (useApiKey) headers["X-API-Key"] = API_KEY;
      if (auth) {
        if (!state.accessToken) throw { message: "Sesi tidak ditemukan, silakan login ulang." };
        headers["Authorization"] = "Bearer " + state.accessToken;
      }
      
      let url = BASE + path;
      if (query) url += "?" + new URLSearchParams(query).toString();
      
      const res = await fetch(url, {
        method,
        headers,
        body: isForm ? body : (body ? JSON.stringify(body) : undefined)
      });
      
      let data = null;
      try { data = await res.json(); } catch (e) {}
      
      if (!res.ok) {
        // Auto-refresh sekali kalau 401 dan ini bukan retry
        if (res.status === 401 && auth && !_retry && state.refreshToken) {
          try {
            if (!isRefreshing) {
              isRefreshing = true;
              await refreshAccessToken();
              isRefreshing = false;
            } else {
              // tunggu refresh yang sedang berjalan
              await new Promise(r => {
                const check = setInterval(() => {
                  if (!isRefreshing) {
                    clearInterval(check);
                    r();
                  }
                }, 150);
              });
            }
            return apiCall(path, { method, body, auth, useApiKey, isForm, query, _retry: true });
          } catch (refreshErr) {
            isRefreshing = false;
            clearSession();
            updateNavVisibility();
            showView("login");
            toastWarn("Sesi Berakhir", "Silakan login kembali.");
            throw { status: 401, message: "Sesi berakhir, silakan login ulang." };
          }
        }
        
        const err = buildApiError(res.status, data);
        throw err;
      }
      return data;
    }
    
    function buildApiError(status, data) {
      if (status === 422 && data && Array.isArray(data.detail)) {
        const fields = data.detail.map(d => ({
          field: d.loc ? d.loc[d.loc.length - 1] : "unknown",
          msg: d.msg
        }));
        return {
          status,
          data,
          message: fields.map(f => `${f.field}: ${f.msg}`).join(", "),
          fields
        };
      }
      if (status === 429) {
        const retryAfter = data?.retry_after || data?.detail?.retry_after || null;
        return { status, data, message: "Terlalu banyak percobaan. Coba lagi sebentar lagi.", retryAfter };
      }
      const msg = (data && (data.detail || data.message)) || `Terjadi kesalahan (${status})`;
      return { status, data, message: typeof msg === "string" ? msg : JSON.stringify(msg) };
    }
    
    function showDeleteOptions() {
      openModal({
        icon: "fa-trash",
        title: "Hapus Akun",
        text: "Pilih jenis penghapusan. Soft delete masih bisa dipulihkan tim support, hard delete permanen dan tidak bisa dibatalkan.",
        confirmLabel: "Soft Delete",
        onConfirm: () => deleteAccount(false)
      });
      // Tambahkan tombol hard delete terpisah di modal via override setelah openModal
      setTimeout(() => {
        const row = document.querySelector(".modal-sheet .btn-row");
        if (row && !document.getElementById("btnHardDelete")) {
          const hardBtn = document.createElement("button");
          hardBtn.id = "btnHardDelete";
          hardBtn.className = "btn btn-danger";
          hardBtn.style.marginTop = "8px";
          hardBtn.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> Hard Delete (Permanen)';
          hardBtn.onclick = () => {
            closeModal();
            confirmHardDelete();
          };
          row.parentElement.appendChild(hardBtn);
        }
      }, 50);
    }
    
    function confirmHardDelete() {
      openModal({
        icon: "fa-triangle-exclamation",
        title: "Yakin Hard Delete?",
        text: "Ini PERMANEN. Semua data akan hilang selamanya dan tidak bisa dipulihkan.",
        confirmLabel: "Ya, Hapus Permanen",
        onConfirm: () => deleteAccount(true)
      });
    }
    
    function showFieldErrors(err) {
      // bersihkan error lama
      document.querySelectorAll(".field-error").forEach(el => el.remove());
      document.querySelectorAll(".input-wrap input, .input-wrap textarea").forEach(el => el.classList.remove("input-error"));
      
      if (err.fields && err.fields.length) {
        err.fields.forEach(f => {
          // cari input dengan name/id yang mengandung nama field (best-effort)
          const guessIds = [f.field, f.field + "Input"];
          let input = null;
          for (const id of guessIds) {
            input = document.getElementById(id) ||
              document.querySelector(`[id*="${f.field}" i]`);
            if (input) break;
          }
          if (input) {
            input.classList.add("input-error");
            const errEl = document.createElement("div");
            errEl.className = "hint err field-error";
            errEl.textContent = f.msg;
            input.closest(".field").appendChild(errEl);
          }
        });
        toastError("Periksa Input", "Beberapa field belum sesuai.");
      } else {
        toastError("Gagal", err.message);
      }
    }
    
    /* =========================================================
       TOAST SYSTEM (custom alert pengganti alert() bawaan)
    ========================================================= */
    function toast(type, title, msg, duration = 4000) {
      const stack = document.getElementById("toastStack");
      const icons = { success: "fa-circle-check", error: "fa-circle-xmark", warn: "fa-triangle-exclamation", info: "fa-circle-info" };
      const el = document.createElement("div");
      el.className = `toast ${type}`;
      el.innerHTML = `
    <div class="toast-icon"><i class="fa-solid ${icons[type]}"></i></div>
    <div class="toast-content">
      <div class="toast-title">${title}</div>
      <div class="toast-msg">${msg}</div>
    </div>
    <button class="toast-close"><i class="fa-solid fa-xmark"></i></button>
  `;
      stack.appendChild(el);
      const remove = () => {
        el.classList.add("hide");
        setTimeout(() => el.remove(), 280);
      };
      el.querySelector(".toast-close").onclick = remove;
      setTimeout(remove, duration);
    }
    const toastSuccess = (t, m) => toast("success", t, m);
    const toastError = (t, m) => toast("error", t, m);
    const toastWarn = (t, m) => toast("warn", t, m);
    const toastInfo = (t, m) => toast("info", t, m);
    
    /* =========================================================
       CONFIRM MODAL
    ========================================================= */
    let modalConfirmCallback = null;
    
    function openModal({ icon = "fa-triangle-exclamation", title, text, confirmLabel = "Ya, Lanjutkan", onConfirm }) {
      document.getElementById("modalIcon").innerHTML = `<i class="fa-solid ${icon}"></i>`;
      document.getElementById("modalTitle").textContent = title;
      document.getElementById("modalText").textContent = text;
      const btn = document.getElementById("modalConfirmBtn");
      btn.textContent = confirmLabel;
      modalConfirmCallback = onConfirm;
      document.getElementById("modalOverlay").classList.add("show");
    }
    
    function closeModal() { document.getElementById("modalOverlay").classList.remove("show"); }
    document.getElementById("modalConfirmBtn").addEventListener("click", () => {
      if (modalConfirmCallback) modalConfirmCallback();
      closeModal();
    });
    
    function confirmAction(type) {
      if (type === "deactivate") {
        openModal({
          icon: "fa-pause",
          title: "Nonaktifkan Akun?",
          text: "Akunmu akan dinonaktifkan sementara. Kamu bisa mengaktifkannya kembali nanti.",
          confirmLabel: "Nonaktifkan",
          onConfirm: deactivateAccount
        });
      } else if (type === "delete") {
        openModal({
          icon: "fa-trash",
          title: "Hapus Akun Permanen?",
          text: "Tindakan ini tidak dapat dibatalkan. Semua data kamu akan dihapus.",
          confirmLabel: "Hapus Akun",
          onConfirm: deleteAccount
        });
      } else if (type === "deleteAvatar") {
        openModal({
          icon: "fa-trash",
          title: "Hapus Foto Profil?",
          text: "Foto profil kamu akan dikembalikan ke default.",
          confirmLabel: "Hapus",
          onConfirm: deleteAvatar
        });
      } else if (type === "logoutAll") {
        openModal({
          icon: "fa-power-off",
          title: "Keluar dari Semua Perangkat?",
          text: "Semua sesi aktif termasuk perangkat ini akan diakhiri.",
          confirmLabel: "Ya, Keluar Semua",
          onConfirm: logoutAll
        });
      } else if (type.startsWith("revoke:")) {
        const sid = type.split(":")[1];
        openModal({
          icon: "fa-desktop",
          title: "Cabut Sesi Ini?",
          text: "Perangkat tersebut akan otomatis logout.",
          confirmLabel: "Cabut Sesi",
          onConfirm: () => revokeSession(sid)
        });
      }
    }
    
    /* =========================================================
       PAGE LOADER
    ========================================================= */
    function showLoader() { document.getElementById("pageLoader").classList.add("show"); }
    
    function hideLoader() { document.getElementById("pageLoader").classList.remove("show"); }
    
    async function deleteAvatar() {
      showLoader();
      try {
        await apiCall("/profile/avatar", { method: "DELETE", auth: true });
        toastSuccess("Berhasil", "Foto profil telah dihapus.");
        loadProfile();
      } catch (err) {
        toastError("Gagal Menghapus", err.message);
      } finally { hideLoader(); }
    }
    
    async function uploadDocument(file) {
      if (!file) return;
      const btn = document.getElementById("btnUploadDoc");
      setBtnLoading(btn, true);
      try {
        const form = new FormData();
        form.append("file", file);
        const data = await apiCall("/profile/upload", { method: "POST", auth: true, isForm: true, body: form });
        toastSuccess("Berhasil Diunggah", "Dokumen kamu telah tersimpan.");
        document.getElementById("uploadedDocInfo").innerHTML = `<i class="fa-solid fa-circle-check" style="color:var(--success)"></i> ${file.name} berhasil diunggah`;
      } catch (err) {
        toastError("Gagal Mengunggah", err.message);
      } finally { setBtnLoading(btn, false); }
    }
    
    /* =========================================================
       BUTTON LOADING HELPER
    ========================================================= */
    function setBtnLoading(btn, loading) {
      if (!btn) return;
      btn.disabled = loading;
      btn.classList.toggle("loading", loading);
    }
    
    /* =========================================================
       VIEW ROUTER
    ========================================================= */
    const protectedViews = ["home", "profile", "security", "terms"];
    
    function showView(name) {
      document.querySelectorAll(".view").forEach(v => v.classList.remove("active"));
      const target = document.getElementById("view-" + name);
      if (target) target.classList.add("active");
      document.querySelectorAll(".nav-item").forEach(n => n.classList.toggle("active", n.dataset.nav === name));
      window.scrollTo({ top: 0, behavior: "smooth" });
      
      if (name === "home") loadDashboard();
      if (name === "profile") loadProfile();
      if (name === "security") {
        loadMfaStatus();
        loadSessions();
      }
      if (name === "terms") loadTerms();
    }
    
    function updateNavVisibility() {
      const loggedIn = !!state.accessToken;
      document.getElementById("bottomNav").style.display = loggedIn ? "flex" : "none";
      renderTopbarActions(loggedIn);
    }
    
    function renderTopbarActions(loggedIn) {
      const el = document.getElementById("topbarActions");
      if (loggedIn) {
        el.innerHTML = `<button class="icon-btn" onclick="confirmLogout()"><i class="fa-solid fa-right-from-bracket"></i></button>`;
      } else {
        el.innerHTML = "";
      }
    }
    
    function confirmLogout() {
      openModal({
        icon: "fa-right-from-bracket",
        title: "Keluar dari akun?",
        text: "Kamu perlu login kembali untuk mengakses akunmu.",
        confirmLabel: "Ya, Keluar",
        onConfirm: logout
      });
    }
    
    /* =========================================================
       PASSWORD VISIBILITY TOGGLE
    ========================================================= */
    document.querySelectorAll(".toggle-eye").forEach(btn => {
      btn.addEventListener("click", () => {
        const input = document.getElementById(btn.dataset.toggle);
        const icon = btn.querySelector("i");
        if (input.type === "password") {
          input.type = "text";
          icon.className = "fa-solid fa-eye-slash";
        }
        else {
          input.type = "password";
          icon.className = "fa-solid fa-eye";
        }
      });
    });
    
    /* =========================================================
       PASSWORD STRENGTH
    ========================================================= */
    function checkStrength(val) {
      let score = 0;
      if (val.length >= 8) score++;
      if (/[A-Z]/.test(val)) score++;
      if (/[0-9]/.test(val)) score++;
      if (/[^A-Za-z0-9]/.test(val)) score++;
      const fill = document.getElementById("strengthFill");
      const label = document.getElementById("strengthLabel");
      const levels = [
        { w: "10%", c: "var(--danger)", l: "Sangat lemah" },
        { w: "35%", c: "var(--danger)", l: "Lemah" },
        { w: "60%", c: "var(--warn)", l: "Cukup" },
        { w: "85%", c: "var(--success)", l: "Kuat" },
        { w: "100%", c: "var(--success)", l: "Sangat kuat" }
      ];
      const lv = levels[score];
      fill.style.width = lv.w;
      fill.style.background = lv.c;
      label.textContent = lv.l;
      label.style.color = lv.c;
    }
    
    /* =========================================================
       TABS (passwordless)
    ========================================================= */
    function switchTab(tab) {
      document.querySelectorAll(".tab-btn").forEach(b => b.classList.toggle("active", b.dataset.tab === tab));
      document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));
      document.getElementById("tab-" + tab).classList.add("active");
    }
    
    /* OTP box auto-advance */
    document.querySelectorAll(".otp-box").forEach((box, i, arr) => {
      box.addEventListener("input", () => {
        box.value = box.value.replace(/[^0-9]/g, "");
        if (box.value && arr[i + 1]) arr[i + 1].focus();
      });
      box.addEventListener("keydown", (e) => {
        if (e.key === "Backspace" && !box.value && arr[i - 1]) arr[i - 1].focus();
      });
    });
    
    /* =========================================================
       AUTH: REGISTER
    ========================================================= */
    document.getElementById("formRegister").addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = e.target.querySelector("button[type=submit]");
      const email = document.getElementById("regEmail").value.trim();
      const password = document.getElementById("regPassword").value;
      if (!validateOrToast([
          { valid: isValidEmail(email), msg: "Format email tidak valid." },
          { valid: password.length >= 8, msg: "Password minimal 8 karakter." }
        ])) return;
      setBtnLoading(btn, true);
      try {
        await apiCall("/auth/register", { method: "POST", useApiKey: true, body: { email, password } });
        state.pendingEmail = email;
        toastSuccess("Pendaftaran Berhasil", "Cek email kamu untuk verifikasi akun.");
        document.getElementById("verifyToken").value = "";
        showView("verify");
      } catch (err) {
        showFieldErrors(err);
      } finally { setBtnLoading(btn, false); }
    });
    
    /* =========================================================
       AUTH: LOGIN
    ========================================================= */
    document.getElementById("formLogin").addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = e.target.querySelector("button[type=submit]");
      const email = document.getElementById("loginEmail").value.trim();
      const password = document.getElementById("loginPassword").value;
      
      setBtnLoading(btn, true);
      try {
        const data = await apiCall("/auth/login", { method: "POST", useApiKey: true, body: { email, password } });
        saveSession(data);
        toastSuccess("Berhasil Masuk", "Selamat datang kembali!");
        updateNavVisibility();
        showView("home");
      } catch (err) {
        if (!handleRateLimit(err, btn)) showFieldErrors(err);
      } finally { setBtnLoading(btn, false); }
    });
    
    function saveSession(data) {
      state.accessToken = data.access_token || data.accessToken;
      state.refreshToken = data.refresh_token || data.refreshToken;
      if (state.accessToken) localStorage.setItem("caca_access_token", state.accessToken);
      if (state.refreshToken) localStorage.setItem("caca_refresh_token", state.refreshToken);
    }
    
    /* =========================================================
       AUTH: REFRESH TOKEN
    ========================================================= */
    async function refreshAccessToken() {
      if (!state.refreshToken) throw { message: "Tidak ada refresh token" };
      const data = await apiCall("/auth/refresh", {
        method: "POST",
        useApiKey: true,
        query: { refresh_token: state.refreshToken }
      });
      saveSession(data);
      return data;
    }
    
    function handleRateLimit(err, btn) {
      if (err.status !== 429) return false;
      let seconds = err.retryAfter || 30;
      setBtnLoading(btn, false);
      btn.disabled = true;
      const label = btn.querySelector(".btn-label");
      const originalText = label.textContent;
      const tick = setInterval(() => {
        label.textContent = `Coba lagi dalam ${seconds}s`;
        seconds--;
        if (seconds < 0) {
          clearInterval(tick);
          label.textContent = originalText;
          btn.disabled = false;
        }
      }, 1000);
      toastWarn("Terlalu Banyak Percobaan", "Tunggu sebentar sebelum mencoba lagi.");
      return true;
    }
    
    /* =========================================================
       AUTH: LOGOUT / LOGOUT-ALL
    ========================================================= */
    async function logout() {
      showLoader();
      try {
        await apiCall("/auth/logout", { method: "POST", body: { access_token: state.accessToken, refresh_token: state.refreshToken } });
      } catch (e) {}
      finally {
        clearSession();
        hideLoader();
        toastInfo("Sampai Jumpa", "Kamu telah keluar dari akun.");
        updateNavVisibility();
        showView("login");
      }
    }
    
    async function logoutAll() {
      showLoader();
      try {
        await apiCall("/auth/logout-all", { method: "POST", auth: true });
        toastSuccess("Berhasil", "Semua sesi telah diakhiri.");
      } catch (err) {
        toastError("Gagal", err.message);
      } finally {
        clearSession();
        hideLoader();
        updateNavVisibility();
        showView("login");
      }
    }
    
    function clearSession() {
      state.accessToken = null;
      state.refreshToken = null;
      state.user = null;
      localStorage.removeItem("caca_access_token");
      localStorage.removeItem("caca_refresh_token");
    }
    
    /* =========================================================
       AUTH: VERIFY EMAIL / RESEND
    ========================================================= */
    document.getElementById("formVerifyEmail").addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = e.target.querySelector("button[type=submit]");
      const token = document.getElementById("verifyToken").value.trim();
      setBtnLoading(btn, true);
      try {
        await apiCall("/auth/verify-email", { method: "POST", useApiKey: true, body: { token } });
        toastSuccess("Email Terverifikasi", "Akunmu sudah aktif sepenuhnya.");
        showView("login");
      } catch (err) {
        showFieldErrors(err);
      } finally { setBtnLoading(btn, false); }
    });
    
    async function resendVerification() {
      const btn = document.getElementById("btnResend");
      const email = state.pendingEmail || document.getElementById("regEmail").value || document.getElementById("loginEmail").value;
      if (!email) { toastWarn("Email Diperlukan", "Isi email di form login/daftar terlebih dahulu."); return; }
      setBtnLoading(btn, true);
      try {
        await apiCall("/auth/resend-verification", { method: "POST", useApiKey: true, body: { email } });
        toastSuccess("Terkirim", "Email verifikasi baru telah dikirim.");
      } catch (err) {
        if (!handleRateLimit(err, btn)) toastError("Gagal Mengirim", err.message);
      } finally { setBtnLoading(btn, false); }
    }
    
    function isValidEmail(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v); }
    
    function validateOrToast(rules) {
      for (const r of rules) {
        if (!r.valid) { toastWarn("Periksa Kembali", r.msg); return false; }
      }
      return true;
    }
    /* =========================================================
       AUTH: FORGOT / RESET PASSWORD
    ========================================================= */
    document.getElementById("formForgot").addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = e.target.querySelector("button[type=submit]");
      const email = document.getElementById("forgotEmail").value.trim();
      setBtnLoading(btn, true);
      try {
        await apiCall("/auth/forgot-password", { method: "POST", useApiKey: true, body: { email } });
        toastSuccess("Terkirim", "Tautan reset password telah dikirim ke email.");
      } catch (err) {
        if (!handleRateLimit(err, btn)) showFieldErrors(err);
      } finally { setBtnLoading(btn, false); }
    });
    
    document.getElementById("formReset").addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = e.target.querySelector("button[type=submit]");
      const token = document.getElementById("resetToken").value.trim();
      const new_password = document.getElementById("resetNewPassword").value;
      if (!validateOrToast([
          { valid: resetToken.length > 0, msg: "Token tidak boleh kosong." },
          { valid: new_password.length >= 8, msg: "Password baru minimal 8 karakter." }
        ])) return;
      setBtnLoading(btn, true);
      try {
        await apiCall("/auth/reset-password", { method: "POST", useApiKey: true, body: { token, new_password } });
        toastSuccess("Password Diperbarui", "Silakan login dengan password baru.");
        showView("login");
      } catch (err) {
        showFieldErrors(err);
      } finally { setBtnLoading(btn, false); }
    });
    
    /* =========================================================
       AUTH: CHANGE PASSWORD
    ========================================================= */
    document.getElementById("formChangePassword").addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = e.target.querySelector("button[type=submit]");
      const old_password = document.getElementById("oldPassword").value;
      const new_password = document.getElementById("newPassword").value;
      if (!validateOrToast([
          { valid: old_password !== new_password, msg: "Password baru harus berbeda dari password lama." },
          { valid: new_password.length >= 8, msg: "Password baru minimal 8 karakter." }
        ])) return;
      setBtnLoading(btn, true);
      try {
        await apiCall("/auth/change-password", { method: "POST", auth: true, body: { old_password, new_password } });
        toastSuccess("Berhasil", "Password kamu telah diperbarui.");
        e.target.reset();
      } catch (err) {
        showFieldErrors(err);
      } finally { setBtnLoading(btn, false); }
    });
    
    /* =========================================================
       PASSWORDLESS: MAGIC LINK
    ========================================================= */
    document.getElementById("formMagicRequest").addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = e.target.querySelector("button[type=submit]");
      const email = document.getElementById("magicEmail").value.trim();
      setBtnLoading(btn, true);
      try {
        await apiCall("/auth/magic-link/request", { method: "POST", useApiKey: true, body: { email } });
        toastSuccess("Magic Link Terkirim", "Buka tautan di email untuk masuk otomatis.");
      } catch (err) {
        if (!handleRateLimit(err, btn)) showFieldErrors(err);
      } finally { setBtnLoading(btn, false); }
    });
    
    // Auto-verify jika halaman dibuka dengan ?magic_token=xxx
    async function checkMagicLinkInUrl() {
      const params = new URLSearchParams(window.location.search);
      const token = params.get("magic_token");
      if (!token) return;
      showLoader();
      try {
        const data = await apiCall("/auth/magic-link/verify", { method: "POST", useApiKey: true, body: { token } });
        saveSession(data);
        toastSuccess("Berhasil Masuk", "Login via magic link berhasil.");
        updateNavVisibility();
        showView("home");
      } catch (err) {
        toastError("Magic Link Tidak Valid", err.message);
      } finally { hideLoader(); }
    }
    
    /* =========================================================
       PASSWORDLESS: OTP
    ========================================================= */
    document.getElementById("formOtpRequest").addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = e.target.querySelector("button[type=submit]");
      const phone = document.getElementById("otpPhone").value.trim();
      setBtnLoading(btn, true);
      try {
        await apiCall("/auth/otp/request", { method: "POST", useApiKey: true, body: { phone } });
        state.pendingOtpPhone = phone;
        toastSuccess("Kode Terkirim", "Cek SMS kamu untuk kode OTP.");
        document.getElementById("formOtpRequest").style.display = "none";
        document.getElementById("formOtpVerify").style.display = "block";
      } catch (err) {
        showFieldErrors(err);
      } finally { setBtnLoading(btn, false); }
    });
    
    document.getElementById("formOtpVerify").addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = e.target.querySelector("button[type=submit]");
      const code = Array.from(document.querySelectorAll(".otp-box")).map(b => b.value).join("");
      if (code.length !== 6) { toastWarn("Kode Belum Lengkap", "Masukkan 6 digit kode OTP."); return; }
      setBtnLoading(btn, true);
      try {
        const data = await apiCall("/auth/otp/verify", { method: "POST", useApiKey: true, body: { phone: state.pendingOtpPhone, code } });
        saveSession(data);
        toastSuccess("Berhasil Masuk", "Verifikasi OTP berhasil.");
        updateNavVisibility();
        showView("home");
      } catch (err) {
        if (!handleRateLimit(err, btn)) showFieldErrors(err);
      } finally { setBtnLoading(btn, false); }
    });
    
    /* =========================================================
       PASSWORDLESS: ANONYMOUS
    ========================================================= */
    async function loginAnonymous() {
      const btn = document.getElementById("btnAnon");
      setBtnLoading(btn, true);
      try {
        const data = await apiCall("/auth/anonymous", { method: "POST", useApiKey: true });
        saveSession(data);
        toastSuccess("Masuk sebagai Tamu", "Selamat menjelajah!");
        updateNavVisibility();
        showView("home");
      } catch (err) {
        toastError("Gagal", err.message);
      } finally { setBtnLoading(btn, false); }
    }
    
    /* =========================================================
       OAUTH
    ========================================================= */
    function oauthStart(provider) {
      // redirect browser langsung ke endpoint OAuth start
      window.location.href = `${BASE}/auth/oauth/${provider}/start`;
    }
    // Note: /auth/oauth/{provider}/callback ditangani otomatis oleh backend setelah redirect provider.
    // /auth/oauth/apple/callback perlu form POST khusus dari Apple JS SDK (form-urlencoded), lihat dokumentasi Apple Sign-In.
    
    /* =========================================================
       PROFILE: GET /auth/me + load ke UI
    ========================================================= */
    async function loadDashboard() {
      document.getElementById("homeGreeting").textContent = "Halo 👋";
      try {
        const me = await apiCall("/auth/me", { method: "GET", auth: true });
        state.user = me;
        document.getElementById("homeGreeting").textContent = `Halo, ${me.name || me.email || "Pengguna"} 👋`;
        
        const sessions = await apiCall("/auth/sessions", { method: "GET", auth: true }).catch(() => []);
        document.getElementById("statSessions").textContent = Array.isArray(sessions) ? sessions.length : (sessions.sessions?.length || "-");
        document.getElementById("statMfa").textContent = me.mfa_enabled ? "Aktif" : "Nonaktif";
      } catch (err) {
        toastError("Gagal Memuat", err.message);
      }
    }
    
    async function loadProfile() {
      document.getElementById("avatarPreview").innerHTML = '<div class="skeleton" style="width:100%;height:100%;border-radius:50%;"></div>';
      try {
        const me = await apiCall("/auth/me", { method: "GET", auth: true });
        state.user = me;
        document.getElementById("profileName").textContent = me.name || "Belum diatur";
        document.getElementById("profileEmail").textContent = me.email || "-";
        document.getElementById("avatarPreview").textContent = (me.name || me.email || "?").charAt(0).toUpperCase();
        if (me.avatar_url) {
          document.getElementById("avatarPreview").innerHTML = `<img src="${me.avatar_url}" style="width:100%;height:100%;border-radius:50%;object-fit:cover;">`;
          document.getElementById("btnDeleteAvatar").style.display = "block"; // BARU
        } else {
          document.getElementById("btnDeleteAvatar").style.display = "none"; // BARU
        }
        document.getElementById("profileNameInput").value = me.name || "";
        document.getElementById("profileBioInput").value = me.bio || "";
        document.getElementById("profileBirthInput").value = me.birth_date || "";
        
        const badge = document.getElementById("verifyBadge");
        if (me.email_verified) {
          badge.className = "badge";
          badge.innerHTML = `<i class="fa-solid fa-circle-check"></i> Terverifikasi`;
        } else {
          badge.className = "badge warn";
          badge.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> Belum Terverifikasi`;
        }
        
        // preferences
        const prefs = await apiCall("/profile/preferences", { method: "GET", auth: true }).catch(() => null);
        if (prefs) {
          document.getElementById("prefLanguage").value = prefs.language || "id";
          document.getElementById("prefTimezone").value = prefs.timezone || "Asia/Jakarta";
          document.getElementById("prefNotif").checked = prefs.notifications_enabled !== false;
          document.getElementById("prefPublic").checked = !!prefs.privacy_profile_public;
        }
      } catch (err) {
        toastError("Gagal Memuat Profil", err.message);
      }
    }
    
    /* PATCH /profile */
    document.getElementById("formProfile").addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = e.target.querySelector("button[type=submit]");
      const name = document.getElementById("profileNameInput").value.trim();
      const bio = document.getElementById("profileBioInput").value.trim();
      const birth_date = document.getElementById("profileBirthInput").value;
      setBtnLoading(btn, true);
      try {
        await apiCall("/profile", { method: "PATCH", auth: true, body: { name, bio, birth_date } });
        toastSuccess("Tersimpan", "Profil kamu telah diperbarui.");
        loadProfile();
      } catch (err) {
        showFieldErrors(err);
      } finally { setBtnLoading(btn, false); }
    });
    
    /* POST /profile/avatar (multipart) */
    async function uploadAvatar(file) {
      if (!file) return;
      showLoader();
      try {
        const form = new FormData();
        form.append("file", file);
        await apiCall("/profile/avatar", { method: "POST", auth: true, isForm: true, body: form });
        toastSuccess("Avatar Diperbarui", "Foto profil kamu berhasil diubah.");
        loadProfile();
      } catch (err) {
        toastError("Gagal Upload", err.message);
      } finally { hideLoader(); }
    }
    
    /* PATCH /profile/preferences */
    async function savePreferences() {
      const btn = document.getElementById("btnSavePref");
      setBtnLoading(btn, true);
      try {
        await apiCall("/profile/preferences", {
          method: "PATCH",
          auth: true,
          body: {
            language: document.getElementById("prefLanguage").value,
            timezone: document.getElementById("prefTimezone").value,
            notifications_enabled: document.getElementById("prefNotif").checked,
            privacy_profile_public: document.getElementById("prefPublic").checked
          }
        });
        toastSuccess("Preferensi Disimpan", "Pengaturan kamu telah diperbarui.");
      } catch (err) {
        toastError("Gagal Menyimpan", err.message);
      } finally { setBtnLoading(btn, false); }
    }
    
    /* POST /profile/change-email/request */
    document.getElementById("formChangeEmail").addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = e.target.querySelector("button[type=submit]");
      const new_email = document.getElementById("newEmailInput").value.trim();
      setBtnLoading(btn, true);
      try {
        await apiCall("/profile/change-email/request", { method: "POST", auth: true, body: { new_email } });
        toastSuccess("Konfirmasi Terkirim", "Cek email baru kamu untuk konfirmasi perubahan.");
        e.target.reset();
      } catch (err) {
        showFieldErrors(err);
      } finally { setBtnLoading(btn, false); }
    });
    
    /* POST /profile/deactivate & DELETE /profile/delete */
    async function deactivateAccount() {
      showLoader();
      try {
        await apiCall("/profile/deactivate", { method: "POST", auth: true });
        toastInfo("Akun Dinonaktifkan", "Kamu bisa mengaktifkannya kembali kapan saja.");
        clearSession();
        updateNavVisibility();
        showView("login");
      } catch (err) {
        toastError("Gagal", err.message);
      } finally { hideLoader(); }
    }
    
    async function deleteAccount(hard = false) {
      showLoader();
      try {
        await apiCall("/profile/delete", { method: "DELETE", auth: true, query: { hard } });
        toastInfo(hard ? "Akun Dihapus Permanen" : "Akun Dihapus", hard ? "Semua data telah dihapus permanen." : "Data akun dinonaktifkan.");
        clearSession();
        updateNavVisibility();
        showView("login");
      } catch (err) {
        toastError("Gagal Menghapus", err.message);
      } finally { hideLoader(); }
    }
    
    /* =========================================================
       MFA / TOTP
    ========================================================= */
    async function loadMfaStatus() {
      try {
        const me = state.user || await apiCall("/auth/me", { method: "GET", auth: true });
        if (me.mfa_enabled) {
          document.getElementById("mfaNotSetup").style.display = "none";
          document.getElementById("mfaSetupPanel").style.display = "none";
          document.getElementById("mfaActivePanel").style.display = "block";
        } else {
          document.getElementById("mfaNotSetup").style.display = "block";
          document.getElementById("mfaSetupPanel").style.display = "none";
          document.getElementById("mfaActivePanel").style.display = "none";
        }
      } catch (err) {}
    }
    
    async function setupTotp() {
      const btn = document.getElementById("btnSetupTotp");
      setBtnLoading(btn, true);
      try {
        const data = await apiCall("/mfa/totp/setup", { method: "POST", auth: true });
        state.totpSecret = data.secret;
        document.getElementById("totpQr").src = data.qr_code_url || data.qr_url || "";
        document.getElementById("totpSecret").textContent = data.secret || "-";
        document.getElementById("mfaNotSetup").style.display = "none";
        document.getElementById("mfaSetupPanel").style.display = "block";
      } catch (err) {
        toastError("Gagal Setup MFA", err.message);
      } finally { setBtnLoading(btn, false); }
    }
    
    function copySecret() {
      navigator.clipboard.writeText(document.getElementById("totpSecret").textContent);
      toastInfo("Disalin", "Secret key disalin ke clipboard.");
    }
    
    document.getElementById("formEnableTotp").addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = e.target.querySelector("button[type=submit]");
      const code = document.getElementById("totpEnableCode").value.trim();
      setBtnLoading(btn, true);
      try {
        await apiCall("/mfa/totp/enable", { method: "POST", auth: true, body: { code } });
        toastSuccess("MFA Aktif", "Autentikasi dua faktor berhasil diaktifkan.");
        document.getElementById("mfaSetupPanel").style.display = "none";
        document.getElementById("mfaActivePanel").style.display = "block";
      } catch (err) {
        if (!handleRateLimit(err, btn)) showFieldErrors(err);
      } finally { setBtnLoading(btn, false); }
    });
    
    document.getElementById("formDisableTotp").addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = e.target.querySelector("button[type=submit]");
      const code = document.getElementById("totpDisableCode").value.trim();
      setBtnLoading(btn, true);
      try {
        await apiCall("/mfa/totp/disable", { method: "POST", auth: true, body: { code } });
        toastInfo("MFA Dinonaktifkan", "Autentikasi dua faktor telah dimatikan.");
        document.getElementById("mfaActivePanel").style.display = "none";
        document.getElementById("mfaNotSetup").style.display = "block";
      } catch (err) {
        if (!handleRateLimit(err, btn)) showFieldErrors(err);
      } finally { setBtnLoading(btn, false); }
    });
    
    /* =========================================================
       SESSIONS
    ========================================================= */
    async function loadSessions() {
      const container = document.getElementById("sessionList");
      container.innerHTML = `<div class="empty-state"><i class="fa-solid fa-spinner fa-spin"></i><p>Memuat sesi...</p></div>`;
      try {
        const res = await apiCall("/auth/sessions", { method: "GET", auth: true });
        const sessions = Array.isArray(res) ? res : (res.sessions || []);
        if (!sessions.length) {
          container.innerHTML = `<div class="empty-state"><i class="fa-solid fa-desktop"></i><p>Tidak ada sesi aktif lain.</p></div>`;
          return;
        }
        container.innerHTML = sessions.map(s => `
      <div class="session-item">
        <div class="session-icon"><i class="fa-solid ${s.device_type === 'mobile' ? 'fa-mobile-screen' : 'fa-desktop'}"></i></div>
        <div class="session-body">
          <div class="session-device">${s.device || s.user_agent || "Perangkat Tidak Dikenal"}</div>
          <div class="session-meta">${s.location || s.ip_address || ""} · ${s.last_active || s.created_at || ""}</div>
          ${s.is_current ? '<div class="session-current"><i class="fa-solid fa-circle"></i> Sesi ini</div>' : ""}
        </div>
        ${!s.is_current ? `<button class="session-revoke" onclick="confirmAction('revoke:${s.id || s.session_id}')"><i class="fa-solid fa-xmark"></i></button>` : ""}
      </div>
    `).join("");
      } catch (err) {
        container.innerHTML = `<div class="empty-state"><i class="fa-solid fa-triangle-exclamation"></i><p>Gagal memuat sesi.</p></div>`;
      }
    }
    
    async function revokeSession(sessionId) {
      showLoader();
      try {
        await apiCall(`/auth/sessions/${sessionId}`, { method: "DELETE", auth: true });
        toastSuccess("Sesi Dicabut", "Perangkat tersebut telah keluar.");
        loadSessions();
      } catch (err) {
        toastError("Gagal Mencabut Sesi", err.message);
      } finally { hideLoader(); }
    }
    
    /* =========================================================
       TERMS
    ========================================================= */
    async function loadTerms() {
      try {
        const latest = await apiCall("/terms/latest", { method: "GET" });
        document.getElementById("termsContentBox").textContent = latest.content || "Tidak ada konten.";
        window._latestTermsVersion = latest.version;
      } catch (err) {
        document.getElementById("termsContentBox").textContent = "Gagal memuat konten terms.";
      }
      try {
        const status = await apiCall("/terms/status", { method: "GET", auth: true });
        const box = document.getElementById("termsStatusBox");
        if (status.accepted) {
          box.innerHTML = `<span style="color:var(--success);"><i class="fa-solid fa-circle-check"></i> Sudah disetujui (v${status.version || "-"})</span>`;
        } else {
          box.innerHTML = `<span style="color:var(--warn);"><i class="fa-solid fa-triangle-exclamation"></i> Belum menyetujui versi terbaru</span>`;
        }
      } catch (err) {
        document.getElementById("termsStatusBox").textContent = "Gagal memuat status.";
      }
    }
    
    async function acceptTerms() {
      const btn = document.getElementById("btnAcceptTerms");
      setBtnLoading(btn, true);
      try {
        await apiCall("/terms/accept", { method: "POST", auth: true, body: { version: window._latestTermsVersion || "1.0" } });
        toastSuccess("Disetujui", "Terima kasih telah menyetujui syarat & ketentuan.");
        loadTerms();
      } catch (err) {
        toastError("Gagal", err.message);
      } finally { setBtnLoading(btn, false); }
    }
    
    /* =========================================================
       INIT
    ========================================================= */
    (async function init() {
      await checkMagicLinkInUrl();
      updateNavVisibility();
      if (state.accessToken) {
        showView("home");
      } else {
        showView("login");
      }
    })();
  </script>
  
</body>

</html>
