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

class SignupScreen extends ConsumerStatefulWidget {
  const SignupScreen({super.key});

  @override
  ConsumerState<SignupScreen> createState() => _SignupScreenState();
}

class _SignupScreenState extends ConsumerState<SignupScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _usernameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmController = TextEditingController();
  bool _obscurePassword = true;
  bool _obscureConfirm = true;
  bool _isLoading = false;

  @override
  void dispose() {
    _nameController.dispose();
    _usernameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    _confirmController.dispose();
    super.dispose();
  }

  Future<void> _signup() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _isLoading = true);

    try {
      await ref.read(authProvider.notifier).register(
        email: _emailController.text.trim(),
        password: _passwordController.text,
        displayName: _nameController.text.trim(),
        username: _usernameController.text.trim().toLowerCase(),
      );
      if (mounted) context.go(BrewdriftRoutes.onboarding);
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
                  'Start your\ncafé story.',
                  style: AppTypography.displayMedium,
                ).animate().fadeIn(duration: 500.ms).slideY(begin: 0.2, end: 0, duration: 500.ms),

                const SizedBox(height: AppSpacing.sm),

                Text(
                  'Create your Brewdrift account.',
                  style: AppTypography.caption.copyWith(fontSize: 16),
                ).animate().fadeIn(delay: 100.ms, duration: 500.ms),

                const SizedBox(height: AppSpacing.xl),

                BrewTextField(
                  controller: _nameController,
                  label: 'Full Name',
                  hint: 'Your name',
                  textInputAction: TextInputAction.next,
                  prefixIcon: const Icon(Icons.person_outline_rounded),
                  validator: (v) {
                    if (v == null || v.trim().isEmpty) return 'Enter your name';
                    if (v.trim().length < 2) return 'Name is too short';
                    return null;
                  },
                ).animate().fadeIn(delay: 200.ms, duration: 400.ms),

                const SizedBox(height: AppSpacing.md),

                BrewTextField(
                  controller: _usernameController,
                  label: 'Username',
                  hint: '@yourhandle',
                  textInputAction: TextInputAction.next,
                  prefixIcon: const Icon(Icons.alternate_email_rounded),
                  validator: (v) {
                    if (v == null || v.trim().isEmpty) return 'Enter a username';
                    final clean = v.trim().toLowerCase();
                    if (clean.length < 3) return 'Username must be 3+ characters';
                    if (!RegExp(r'^[a-z0-9_]+$').hasMatch(clean)) {
                      return 'Only letters, numbers and underscores';
                    }
                    return null;
                  },
                ).animate().fadeIn(delay: 250.ms, duration: 400.ms),

                const SizedBox(height: AppSpacing.md),

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
                ).animate().fadeIn(delay: 300.ms, duration: 400.ms),

                const SizedBox(height: AppSpacing.md),

                BrewTextField(
                  controller: _passwordController,
                  label: 'Password',
                  hint: 'At least 8 characters',
                  obscureText: _obscurePassword,
                  textInputAction: TextInputAction.next,
                  prefixIcon: const Icon(Icons.lock_outline_rounded),
                  suffixIcon: IconButton(
                    icon: Icon(
                      _obscurePassword ? Icons.visibility_outlined : Icons.visibility_off_outlined,
                      color: AppColors.mochaMedium,
                      size: 20,
                    ),
                    onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
                  ),
                  validator: (v) {
                    if (v == null || v.isEmpty) return 'Enter a password';
                    if (v.length < 8) return 'Password must be at least 8 characters';
                    if (!RegExp(r'(?=.*[A-Z])').hasMatch(v)) {
                      return 'Include at least one uppercase letter';
                    }
                    if (!RegExp(r'(?=.*[0-9])').hasMatch(v)) {
                      return 'Include at least one number';
                    }
                    return null;
                  },
                ).animate().fadeIn(delay: 350.ms, duration: 400.ms),

                const SizedBox(height: AppSpacing.xs),

                // Password requirements hint
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 4),
                  child: Text(
                    'Min. 8 characters · 1 uppercase · 1 number',
                    style: AppTypography.labelSmall.copyWith(
                      color: AppColors.mochaMedium.withOpacity(0.7),
                    ),
                  ),
                ),

                const SizedBox(height: AppSpacing.md),

                BrewTextField(
                  controller: _confirmController,
                  label: 'Confirm Password',
                  hint: 'Repeat your password',
                  obscureText: _obscureConfirm,
                  textInputAction: TextInputAction.done,
                  onFieldSubmitted: (_) => _signup(),
                  prefixIcon: const Icon(Icons.lock_outline_rounded),
                  suffixIcon: IconButton(
                    icon: Icon(
                      _obscureConfirm ? Icons.visibility_outlined : Icons.visibility_off_outlined,
                      color: AppColors.mochaMedium,
                      size: 20,
                    ),
                    onPressed: () => setState(() => _obscureConfirm = !_obscureConfirm),
                  ),
                  validator: (v) {
                    if (v == null || v.isEmpty) return 'Confirm your password';
                    if (v != _passwordController.text) return 'Passwords do not match';
                    return null;
                  },
                ).animate().fadeIn(delay: 400.ms, duration: 400.ms),

                const SizedBox(height: AppSpacing.xl),

                BrewButton(
                  text: 'Create Account',
                  onPressed: _signup,
                  isLoading: _isLoading,
                ).animate().fadeIn(delay: 450.ms, duration: 400.ms),

                const SizedBox(height: AppSpacing.xl),

                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text('Already have an account? ', style: AppTypography.bodyMedium),
                    GestureDetector(
                      onTap: () => context.go(BrewdriftRoutes.login),
                      child: Text(
                        'Log In',
                        style: AppTypography.labelLarge.copyWith(
                          color: AppColors.caramel,
                          decoration: TextDecoration.underline,
                          decorationColor: AppColors.caramel,
                        ),
                      ),
                    ),
                  ],
                ).animate().fadeIn(delay: 500.ms, duration: 400.ms),

                const SizedBox(height: AppSpacing.xl),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
