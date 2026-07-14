# AWS EC2 Deployment Guide

Here is the step-by-step guide to deploying your new Streamlit RAG application on AWS from scratch. 

> [!NOTE]
> Before deploying, test the app locally by running: 
> `venv\Scripts\python.exe -m pip install streamlit` 
> `venv\Scripts\streamlit.exe run app_streamlit.py`

## Step 1: Create an AWS Account and Launch an EC2 Instance

1. Go to [aws.amazon.com](https://aws.amazon.com/) and create an account or log in.
2. In the search bar at the top, type **EC2** and click on it.
3. Click the orange **Launch instance** button.
4. **Name:** Give your instance a name (e.g., `RAG-Pipeline`).
5. **Application and OS Images (Amazon Machine Image):** Select **Ubuntu** (the default Ubuntu Server 24.04 LTS is perfect and free-tier eligible).
6. **Instance type:** Select **t2.micro** (this is free-tier eligible).
7. **Key pair (login):** 
   - Click **Create new key pair**.
   - Name it `rag-key`.
   - Leave the defaults (RSA, .pem) and click **Create key pair**.
   - **IMPORTANT:** A `.pem` file will download to your computer. Keep this safe, you need it to connect to your server!

## Step 2: Configure Network Settings (Security Group)

While still on the "Launch an instance" page, scroll down to **Network settings**:
1. Check the boxes for:
   - Allow SSH traffic from Anywhere
   - Allow HTTP traffic from the internet
   - Allow HTTPS traffic from the internet
2. Click **Edit** in the top right of the Network Settings box.
3. Click **Add security group rule** at the bottom.
4. Set the following values:
   - **Type:** Custom TCP
   - **Port range:** `8501` (This is the port Streamlit uses).
   - **Source type:** Anywhere (0.0.0.0/0).
5. Scroll to the bottom and click the orange **Launch instance** button.

## Step 3: Connect to your EC2 Instance

1. Go back to the EC2 Dashboard and click on **Instances (running)**.
2. Select your `RAG-Pipeline` instance.
3. Click the **Connect** button at the top.
4. Go to the **SSH client** tab. It will give you an exact command to run (e.g., `ssh -i "rag-key.pem" ubuntu@ec2-xxx-xxx-xxx.compute-1.amazonaws.com`).
5. Open a new terminal on your Windows machine, navigate to the folder where you downloaded `rag-key.pem`, and run that command. Type `yes` when prompted.

## Step 4: Setup the Server and Transfer Files

Now that you are inside the AWS server terminal:

1. **Update the server:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install python3-pip python3-venv -y
   ```

2. **Transfer your files:**
   The easiest way is to push your project to a GitHub repository and clone it on the server:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```
   *(Alternatively, you can use a tool like WinSCP or the `scp` command to copy files from your computer to the server).*

## Step 5: Install Dependencies and Run

1. **Create a virtual environment on the server:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your API Key:**
   Make sure your `.env` file or `config.py` on the server has your `GOOGLE_API_KEY`. 

4. **Run the application:**
   To keep the application running even after you close your terminal, we use `tmux` (a terminal multiplexer):
   ```bash
   tmux
   streamlit run app_streamlit.py
   ```
   *To exit the tmux screen while leaving it running, press `Ctrl+B`, let go, and then press `D`.*

## Step 6: Access your App!

1. Go back to the AWS EC2 Console.
2. Find the **Public IPv4 address** of your instance.
3. Open your browser and go to: `http://<your-public-ip>:8501`
4. You should see your RAG Chatbot live on the internet!
