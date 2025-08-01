mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
maxUploadSize = 50\n\
\n\
[browser]\n\
gatherUsageStats = false\n\
\n\
[global]\n\
disableWatchdogWarning = true\n\
\n\
[theme]\n\
base = 'light'\n\
\n\
" > ~/.streamlit/config.toml

# Create artifacts directory if it doesn't exist
mkdir -p artifacts
