#!/usr/bin/env python3
# Morrowind AI Framework - Setup Script

from setuptools import setup, find_packages

setup(
    name="morrowind-ai-server",
    version="0.1.0",
    description="AI server for the Morrowind AI Framework",
    author="Morrowind AI Framework Team",
    author_email="example@example.com",
    url="https://github.com/example/morrowind-ai-framework",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "websockets>=10.3",
        "python-dotenv>=0.20.0",
        "tenacity>=8.0.1",
        "openai>=0.27.0",
        "anthropic>=0.2.8",
        "aiohttp>=3.8.3",
        "numpy>=1.22.0",
        "pydantic>=1.9.0",
    ],
    extras_require={
        "voice": [
            "elevenlabs>=0.2.18",
            "pyttsx3>=2.90",
        ],
        "local": [
            "llama-cpp-python>=0.1.65; platform_system != 'Windows'",
            "llama-cpp-python-cuda>=0.1.65; platform_system == 'Windows'",
        ],
    },
    entry_points={
        "console_scripts": [
            "morrowind-ai-server=morrowind_ai_server.run_server:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Games/Entertainment :: Role-Playing",
    ],
)
