from setuptools import setup, find_packages

setup(
    name="riot-api-app",                # Your package name
    version="0.1",
    description="A FastAPI app that integrates with Riot Games API",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),           # Automatically find packages in the project
    include_package_data=True,          # Include other files like .env if specified in MANIFEST.in
    install_requires=[
        "fastapi",                      # The necessary dependencies
        "requests",
        "python-dotenv",
        "uvicorn"
    ],
    entry_points={
        'console_scripts': [
            'riot-api-app=app.main:main',    # Entry point to run the FastAPI app
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
