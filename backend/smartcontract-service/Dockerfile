# Use Eclipse Temurin OpenJDK 17 base image
FROM eclipse-temurin:17-jdk-focal

# Set working directory
WORKDIR /app

# Copy Maven wrapper and pom.xml first to leverage Docker cache
COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .

# Copy source code
COPY src src

# Install Maven and build the project
RUN apt-get update && apt-get install -y maven \
    && ./mvnw clean package -DskipTests \
    && rm -rf /var/lib/apt/lists/*

# Expose port 8080 (Spring Boot default)
EXPOSE 8080

# Set JVM options
ENV JAVA_OPTS="-Xms512m -Xmx1024m"

# Run the Spring Boot application JAR
CMD ["java", "-jar", "target/smartcontract-service-1.0.0.jar"]
