import java.util.Properties

plugins {
    id("com.android.application")
    // The Flutter Gradle Plugin must be applied after the Android and Kotlin Gradle plugins.
    id("dev.flutter.flutter-gradle-plugin")
}

android {
    namespace = "com.brewdrift.brewdrift"
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    defaultConfig {
        // TODO: Specify your own unique Application ID (https://developer.android.com/studio/build/application-id.html).
        applicationId = "com.brewdrift.brewdrift"
        // You can update the following values to match your application needs.
        // For more information, see: https://flutter.dev/to/review-gradle-config.
        minSdk = flutter.minSdkVersion
        targetSdk = flutter.targetSdkVersion
        versionCode = flutter.versionCode
        versionName = flutter.versionName

        val envFile = rootProject.file("../.env")
        val envProperties = Properties()
        if (envFile.exists()) {
            envFile.inputStream().use { envProperties.load(it) }
        }
        val rawApiKey = envProperties.getProperty("GOOGLE_MAPS_ANDROID_API_KEY")
        val mapsApiKey = if (rawApiKey.isNullOrBlank() || rawApiKey == "YOUR_GOOGLE_MAPS_ANDROID_API_KEY_HERE") {
            "AIzaSyDUMMY_KEY_FOR_BREWDRIFT_INITIALIZATION"
        } else {
            rawApiKey
        }
        manifestPlaceholders["GOOGLE_MAPS_ANDROID_API_KEY"] = mapsApiKey
    }

    buildTypes {
        release {
            // TODO: Add your own signing config for the release build.
            // Signing with the debug keys for now, so `flutter run --release` works.
            signingConfig = signingConfigs.getByName("debug")
        }
    }
}

kotlin {
    compilerOptions {
        jvmTarget = org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17
    }
}

flutter {
    source = "../.."
}
