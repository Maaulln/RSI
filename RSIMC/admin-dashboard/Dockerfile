FROM node:18-alpine AS builder

WORKDIR /app

COPY admin-dashboard/package.json ./
RUN npm install

COPY admin-dashboard/ ./
RUN npm run build

FROM node:18-alpine

WORKDIR /app

ENV NODE_ENV=production

COPY --from=builder /app/package.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

EXPOSE 3001

CMD ["npm", "start"]
