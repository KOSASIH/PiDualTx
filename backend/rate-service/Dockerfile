# Use official OpenJDK 17 image as base
FROM eclipse-temurin:17-jdk-focal

# Set working directory inside container
WORKDIR /app

# Copy Maven wrapper and pom.xml first to leverage Docker cache
COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .

# Copy source code
COPY src src

# Install Maven and build the project
RUN apt-get update && apt-get install -y maven && \
    ./mvnw clean package -DskipTests

# Expose port 8080 (default for Spring Boot)
EXPOSE 8080

# Set environment variable for JVM options (optional tuning)
ENV JAVA_OPTS="-Xms512m -Xmx1024m"

# Run the Spring Boot application jar
CMD ["java", "-jar", "target/rate-service-1.0.0.jar"]
