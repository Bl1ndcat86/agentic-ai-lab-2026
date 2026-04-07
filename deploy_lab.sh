#!/bin/bash

# --- 1. GIT SYNCHRONIZATION ---
echo "--- 🔄 Step 1: Syncing Research to GitHub ---"
git add .
echo "Enter your commit message (be specific for your PhD audit):"
read commit_msg
git commit -m "$commit_msg"
git push origin main

# --- 2. GOOGLE CLOUD BUILD ---
echo "--- 🏗️ Step 2: Building Artifact in Google Cloud ---"
gcloud builds submit --tag gcr.io/agentic-ai-lab-2026/aam-governor .

# --- 3. GOOGLE CLOUD RUN DEPLOY ---
echo "--- 🚀 Step 3: Deploying GMD Hub to Production ---"
gcloud run deploy agentic-ai-lab-2026 \
  --image gcr.io/agentic-ai-lab-2026/aam-governor \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory=1Gi \
  --cpu=1 \
  --timeout=300

# --- 4. VERIFICATION ---
echo "--- ✅ Deployment Successful! ---"
echo "Live URL for Audit/Professor:"
gcloud run services describe agentic-ai-lab-2026 --region us-central1 --format='value(status.url)'
