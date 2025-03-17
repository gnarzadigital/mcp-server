FROM n8nio/n8n

# Copy the MCP nodes package
COPY n8n-nodes-mcp/dist /usr/src/app/n8n-nodes-mcp

# Install the MCP nodes
RUN cd /usr/src/app && \
    npm install n8n-nodes-mcp

# Set environment variables
ENV N8N_CUSTOM_EXTENSIONS="/usr/src/app/n8n-nodes-mcp" \
    N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE=true

# Start n8n
CMD ["n8n", "start"] 