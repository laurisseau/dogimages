FROM fluent/fluentd:v1.16-1

# Use root user to install plugins
USER root

# Install plugins (you can add more here as needed)
RUN gem install fluent-plugin-elasticsearch --no-document

# Optional: Install other plugins, for example:
# RUN gem install fluent-plugin-kubernetes_metadata_filter --no-document

# Revert back to fluent user for security
USER fluent
