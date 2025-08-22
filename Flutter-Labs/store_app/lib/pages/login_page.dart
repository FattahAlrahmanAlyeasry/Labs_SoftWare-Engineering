import 'package:flutter/material.dart';

class LoginPage extends StatelessWidget {
  LoginPage({Key? key}) : super(key: key);

  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blueGrey[50], // لون الخلفية
      body: Center(
        child: SingleChildScrollView(
          padding: EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // شعار التطبيق
              FlutterLogo(size: 100),
              SizedBox(height: 40),

              // حقل البريد الإلكتروني
              TextField(
                key: Key('emailField'),
                controller: emailController,
                decoration: InputDecoration(
                  labelText: 'البريد الإلكتروني',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.email),
                ),
              ),
              SizedBox(height: 20),

              // حقل كلمة المرور
              TextField(
                key: Key('passwordField'),
                controller: passwordController,
                obscureText: true,
                decoration: InputDecoration(
                  labelText: 'كلمة المرور',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.lock),
                ),
              ),
              SizedBox(height: 30),

              // زر تسجيل الدخول
              ElevatedButton(
                key: Key('loginButton'),
                onPressed: () {
                  String email = emailController.text;
                  String password = passwordController.text;

                  // هنا يمكنك إضافة وظيفة تسجيل الدخول
                  if (email.isEmpty || password.isEmpty) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('الرجاء ملء جميع الحقول')),
                    );
                  } else {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('تم الضغط على تسجيل الدخول')),
                    );
                  }
                },
                child: Padding(
                  padding: EdgeInsets.symmetric(horizontal: 40, vertical: 12),
                  child: Text(
                    'تسجيل الدخول',
                    style: TextStyle(fontSize: 18),
                  ),
                ),
              ),

              SizedBox(height: 20),

              // نسيت كلمة المرور
              TextButton(
                key: Key('forgotPasswordButton'),
                onPressed: () {
                  Navigator.pushNamed(context, '/forgot_password');
                },
                child: Text('نسيت كلمة المرور؟'),
              ),

              // إنشاء حساب جديد
              TextButton(
                key: Key('signupButton'),
                onPressed: () {
                  Navigator.pushNamed(context, '/signup');
                },
                child: Text('إنشاء حساب جديد'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
