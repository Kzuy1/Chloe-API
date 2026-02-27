FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget \
    gcc \
    g++ \
    build-essential \
    libssl-dev \
    libffi-dev \
    libgl1 \
    libxrender1 \
    libxext6 \
    libxkbcommon0 \
    libxkbcommon-x11-0 \
    libfontconfig1 \
    libxcb1 \
    libxcb-xinerama0 \
    libxcb-render0 \
    libxcb-shape0 \
    libxcb-shm0 \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-image0 \
    libxcb-util1 \
    libxcb-xkb1 \
    libx11-6 \
    libx11-xcb1 \
    libxrandr2 \
    libxi6 \
    libxtst6 \
    libxcomposite1 \
    libxcursor1 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN wget "https://www.opendesign.com/guestfiles/get?filename=ODAFileConverter_QT6_lnxX64_8.3dll_27.1.deb" -O oda.deb \
    && apt-get install -y ./oda.deb \
    && rm oda.deb \
    && ln -s /usr/bin/ODAFileConverter_26.12.0.0/ODAFileConverter /usr/local/bin/ODAFileConverter
    
ENV XDG_RUNTIME_DIR=/tmp/runtime
ENV XDG_CACHE_HOME=/tmp/.cache

RUN mkdir -p /tmp/runtime /tmp/.cache /var/cache/fontconfig \
    && chmod -R 777 /tmp/runtime /tmp/.cache /var/cache/fontconfig

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -u 1000 user \
    && mkdir -p /home/user \
    && chown -R user:user /app /home/user /tmp /var/cache/fontconfig

USER user

CMD ["python", "api.py"]
