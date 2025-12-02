import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:async';

void main() {
  runApp(SantaApp());
}

class SantaApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Santa Wishing Machine',
      theme: ThemeData.dark().copyWith(
        primaryColor: Colors.red,
        scaffoldBackgroundColor: Color(0xFF0D1117),
        accentColor: Colors.redAccent,
      ),
      home: SantaHomePage(),
    );
  }
}

class SantaHomePage extends StatefulWidget {
  @override
  _SantaHomePageState createState() => _SantaHomePageState();
}

class _SantaHomePageState extends State<SantaHomePage> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _niceController = TextEditingController();
  final _naughtyController = TextEditingController();
  final _giftsController = TextEditingController();
  
  String _transcript = '';
  bool _loading = false;
  String _error = '';
  int _imageIndex = 0;
  Timer? _timer;

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  void _startImageRotation() {
    _timer = Timer.periodic(Duration(seconds: 4), (timer) {
      setState(() {
        _imageIndex = (_imageIndex + 1) % 3;
      });
    });
  }

  Future<void> _generateTranscript() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _loading = true;
      _transcript = '';
      _error = '';
    });

    try {
      final response = await http.post(
        Uri.parse('http://localhost:8000/generate-transcript'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'name': _nameController.text,
          'niceItems': _niceController.text,
          'naughtyItems': _naughtyController.text,
          'gifts': _giftsController.text,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          _transcript = data['transcript'];
          _loading = false;
        });
        _startImageRotation();
      } else {
        final data = jsonDecode(response.body);
        setState(() {
          _error = data['detail'] ?? 'An error occurred';
          _loading = false;
        });
      }
    } catch (e) {
      setState(() {
        _error = "Could not connect to the North Pole. Is the server running?";
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Santa Wishing Machine'),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(20),
        child: _transcript.isEmpty ? _buildInputForm() : _buildVideoPlayer(),
      ),
    );
  }

  Widget _buildInputForm() {
    return Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          if (_error.isNotEmpty)
            Container(
              padding: EdgeInsets.all(10),
              margin: EdgeInsets.only(bottom: 20),
              decoration: BoxDecoration(
                color: Colors.red.withOpacity(0.1),
                border: Border.all(color: Colors.red),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Text(_error, style: TextStyle(color: Colors.red)),
            ),
          TextFormField(
            controller: _nameController,
            decoration: InputDecoration(labelText: "Child's Name"),
            validator: (value) => value!.isEmpty ? 'Please enter a name' : null,
          ),
          SizedBox(height: 20),
          TextFormField(
            controller: _niceController,
            decoration: InputDecoration(labelText: "Nice Things Done"),
            maxLines: 3,
          ),
          SizedBox(height: 20),
          TextFormField(
            controller: _naughtyController,
            decoration: InputDecoration(labelText: "Naughty Things Done"),
            maxLines: 3,
          ),
          SizedBox(height: 20),
          TextFormField(
            controller: _giftsController,
            decoration: InputDecoration(labelText: "Gift Wishes"),
            maxLines: 3,
            validator: (value) => value!.isEmpty ? 'Please enter gift wishes' : null,
          ),
          SizedBox(height: 30),
          ElevatedButton(
            onPressed: _loading ? null : _generateTranscript,
            child: _loading ? CircularProgressIndicator() : Text('Generate Video Transcript'),
            style: ElevatedButton.styleFrom(
              primary: Colors.red,
              padding: EdgeInsets.symmetric(vertical: 15),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildVideoPlayer() {
    final images = ['assets/santa1.png', 'assets/santa2.png', 'assets/santa3.png'];
    return Column(
      children: [
        Container(
          height: 300,
          width: double.infinity,
          decoration: BoxDecoration(
            color: Colors.black,
            borderRadius: BorderRadius.circular(12),
          ),
          child: Stack(
            children: [
              // Simulated video player using images
              Center(child: Text('Image: ${images[_imageIndex]}', style: TextStyle(color: Colors.white))), // Placeholder for actual Image.asset
              Positioned(
                bottom: 0,
                left: 0,
                right: 0,
                child: Container(
                  padding: EdgeInsets.all(10),
                  color: Colors.black54,
                  child: Text(
                    _transcript,
                    style: TextStyle(color: Colors.white, fontSize: 16),
                    textAlign: TextAlign.center,
                  ),
                ),
              ),
            ],
          ),
        ),
        SizedBox(height: 20),
        ElevatedButton(
          onPressed: () {
            setState(() {
              _transcript = '';
              _timer?.cancel();
            });
          },
          child: Text('Create Another Message'),
        ),
      ],
    );
  }
}
