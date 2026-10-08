import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/shared/widgets/brew_app_bar.dart';
import 'package:brewdrift/shared/widgets/brew_button.dart';
import 'package:brewdrift/shared/widgets/brew_text_field.dart';
import 'package:brewdrift/shared/widgets/brew_snackbar.dart';
import 'package:google_fonts/google_fonts.dart';

class ForgotPasswordScreen extends StatefulWidget {
  const ForgotPasswordScreen({Key? key}) : super(key: key);

  @override
  State<ForgotPasswordScreen> createState() => _ForgotPasswordScreenState();
}

class _ForgotPasswordScreenState extends State<ForgotPasswordScreen> {
  final _emailController = TextEditingController();
  final _formKey = GlobalKey<FormState>();
  bool _isLoading = false;

  void _submit() async {
    if (_formKey.currentState!.validate()) {
      setState(() => _isLoading = true);
      // Mock API call
      await Future.delayed(const Duration(seconds: 1));
      setState(() => _isLoading = false);
      if (mounted) {
        BrewSnackbar.show(context, 'Check your email for reset instructions.', isSuccess: true);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.softBeige,
      appBar: const BrewAppBar(title: 'Reset Password'),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Forgot your password?',
                style: GoogleFonts.playfairDisplay(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: AppColors.espressoBrown,
                ),
              ),
              const SizedBox(height: 16),
              Text(
                'Enter your email address and we will send you instructions to reset your password.',
                style: GoogleFonts.dmSans(
                  fontSize: 16,
                  color: AppColors.mochaMedium,
                ),
              ),
              const SizedBox(height: 32),
              BrewTextField(
                controller: _emailController,
                label: 'Email',
                hint: 'Enter your email',
                keyboardType: TextInputType.emailAddress,
                validator: (val) => val == null || val.isEmpty ? 'Email is required' : null,
              ),
              const SizedBox(height: 32),
              BrewButton(
                text: 'Send Reset Link',
                isLoading: _isLoading,
                onPressed: _submit,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
