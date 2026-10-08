import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/core/constants/routes.dart';
import 'package:brewdrift/shared/widgets/brew_button.dart';
import 'package:brewdrift/shared/widgets/brew_text_field.dart';
import 'package:brewdrift/shared/widgets/brew_snackbar.dart';
import '../data/auth_repository.dart';

class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _obscurePassword = true;
  bool _isLoading = false;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _login() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _isLoading = true);

    try {
      await ref.read(authProvider.notifier).login(
        email: _emailController.text.trim(),
        password: _passwordController.text,
      );
      if (mounted) context.go(BrewdriftRoutes.home);
    } catch (e) {
      if (mounted) {
        BrewSnackbar.show(context, e.toString(), isError: true);
      }
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.softBeige,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppSpacing.screenPadding),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: AppSpacing.lg),

                // Back button
                GestureDetector(
                  onTap: () => context.go(BrewdriftRoutes.welcome),
                  child: Container(
                    width: 40,
                    height: 40,
                    decoration: BoxDecoration(
                      color: AppColors.warmCream,
                      borderRadius: BorderRadius.circular(AppRadius.sm),
                    ),
                    child: const Icon(
                      Icons.arrow_back_ios_new,
                      size: 18,
                      color: AppColors.espressoBrown,
                    ),
                  ),
                ),

                const SizedBox(height: AppSpacing.xl),

                Text(
                  'Welcome\nback.',
                  style: AppTypography.displayMedium,
                )
                    .animate()
                    .fadeIn(duration: 500.ms)
                    .slideY(begin: 0.2, end: 0, duration: 500.ms),

                const SizedBox(height: AppSpacing.sm),

                Text(
                  'Your café story continues.',
                  style: AppTypography.caption.copyWith(fontSize: 16),
                ).animate().fadeIn(delay: 100.ms, duration: 500.ms),

                const SizedBox(height: AppSpacing.xl),

                // Email field
                BrewTextField(
                  controller: _emailController,
                  label: 'Email',
                  hint: 'your@email.com',
                  keyboardType: TextInputType.emailAddress,
                  textInputAction: TextInputAction.next,
                  prefixIcon: const Icon(Icons.mail_outline_rounded),
                  validator: (v) {
                    if (v == null || v.isEmpty) return 'Enter your email';
                    if (!RegExp(r'^[\w.-]+@[\w.-]+\.\w+$').hasMatch(v)) {
                      return 'Enter a valid email address';
                    }
                    return null;
                  },
                ).animate().fadeIn(delay: 200.ms, duration: 400.ms),

                const SizedBox(height: AppSpacing.md),

                // Password field
                BrewTextField(
                  controller: _passwordController,
                  label: 'Password',
                  hint: 'Your password',
                  obscureText: _obscurePassword,
                  textInputAction: TextInputAction.done,
                  onFieldSubmitted: (_) => _login(),
                  prefixIcon: const Icon(Icons.lock_outline_rounded),
                  suffixIcon: IconButton(
                    icon: Icon(
                      _obscurePassword
                          ? Icons.visibility_outlined
                          : Icons.visibility_off_outlined,
                      color: AppColors.mochaMedium,
                      size: 20,
                    ),
                    onPressed:
                        () =>
                            setState(() => _obscurePassword = !_obscurePassword),
                  ),
                  validator: (v) {
                    if (v == null || v.isEmpty) return 'Enter your password';
                    return null;
                  },
                ).animate().fadeIn(delay: 300.ms, duration: 400.ms),

                const SizedBox(height: AppSpacing.sm),

                // Forgot password
                Align(
                  alignment: Alignment.centerRight,
                  child: TextButton(
                    onPressed:
                        () => context.push(BrewdriftRoutes.forgotPassword),
                    child: Text(
                      'Forgot password?',
                      style: AppTypography.labelMedium.copyWith(
                        color: AppColors.caramel,
                      ),
                    ),
                  ),
                ).animate().fadeIn(delay: 350.ms, duration: 400.ms),

                const SizedBox(height: AppSpacing.lg),

                // Login button
                BrewButton(
                  text: 'Log In',
                  onPressed: _login,
                  isLoading: _isLoading,
                ).animate().fadeIn(delay: 400.ms, duration: 400.ms),

                const SizedBox(height: AppSpacing.xl),

                // Sign up link
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      'New to Brewdrift? ',
                      style: AppTypography.bodyMedium,
                    ),
                    GestureDetector(
                      onTap: () => context.go(BrewdriftRoutes.signup),
                      child: Text(
                        'Create Account',
                        style: AppTypography.labelLarge.copyWith(
                          color: AppColors.caramel,
                          decoration: TextDecoration.underline,
                          decorationColor: AppColors.caramel,
                        ),
                      ),
                    ),
                  ],
                ).animate().fadeIn(delay: 500.ms, duration: 400.ms),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
