import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'dart:io';
import '../../config/theme.dart';
import '../../services/api_service.dart';

class UploadDocumentScreen extends StatefulWidget {
  final String? courseId;

  const UploadDocumentScreen({
    super.key,
    this.courseId,
  });

  @override
  State<UploadDocumentScreen> createState() => _UploadDocumentScreenState();
}

class _UploadDocumentScreenState extends State<UploadDocumentScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _descriptionController = TextEditingController();

  File? _selectedFile;
  String _documentType = 'other';
  bool _isUploading = false;
  bool _isProcessing = false;

  final List<Map<String, String>> _documentTypes = [
    {'value': 'curriculum', 'label': 'Retícula'},
    {'value': 'syllabus', 'label': 'Programa de Materia'},
    {'value': 'reference', 'label': 'Material de Referencia'},
    {'value': 'exercise', 'label': 'Ejercicios'},
    {'value': 'other', 'label': 'Otro'},
  ];

  @override
  void dispose() {
    _nameController.dispose();
    _descriptionController.dispose();
    super.dispose();
  }

  Future<void> _pickFile() async {
    try {
      FilePickerResult? result = await FilePicker.platform.pickFiles(
        type: FileType.custom,
        allowedExtensions: ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'],
      );

      if (result != null) {
        setState(() {
          _selectedFile = File(result.files.single.path!);
          if (_nameController.text.isEmpty) {
            _nameController.text = result.files.single.name;
          }
        });
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error al seleccionar archivo: $e')),
        );
      }
    }
  }

  Future<void> _uploadDocument() async {
    if (!_formKey.currentState!.validate() || _selectedFile == null) {
      return;
    }

    setState(() => _isUploading = true);

    try {
      final apiService = ApiService();

      // Upload document
      final response = await apiService.uploadDocument(
        file: _selectedFile!,
        name: _nameController.text,
        description: _descriptionController.text.isEmpty
            ? null
            : _descriptionController.text,
        documentType: _documentType,
        courseId: widget.courseId,
      );

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Documento subido exitosamente')),
        );

        // Ask if user wants to process with AI
        final shouldProcess = await showDialog<bool>(
          context: context,
          builder: (context) => AlertDialog(
            title: const Text('Procesar con IA'),
            content: const Text(
                '¿Deseas procesar este documento con IA para extraer información?'),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(context, false),
                child: const Text('Ahora no'),
              ),
              ElevatedButton(
                onPressed: () => Navigator.pop(context, true),
                child: const Text('Sí, procesar'),
              ),
            ],
          ),
        );

        if (shouldProcess == true) {
          await _processDocument(response['id']);
        } else {
          Navigator.pop(context, true);
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e')),
        );
      }
    } finally {
      if (mounted) {
        setState(() => _isUploading = false);
      }
    }
  }

  Future<void> _processDocument(String documentId) async {
    setState(() => _isProcessing = true);

    try {
      final apiService = ApiService();
      final result = await apiService.processDocument(documentId);

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Documento procesado con IA')),
        );

        // Show results dialog
        await showDialog(
          context: context,
          builder: (context) => AlertDialog(
            title: const Text('Procesamiento Completado'),
            content: SingleChildScrollView(
              child: Text(result['message'] ?? 'Procesado exitosamente'),
            ),
            actions: [
              ElevatedButton(
                onPressed: () {
                  Navigator.pop(context);
                  Navigator.pop(context, true);
                },
                child: const Text('OK'),
              ),
            ],
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error procesando: $e')),
        );
        Navigator.pop(context, true);
      }
    } finally {
      if (mounted) {
        setState(() => _isProcessing = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Subir Documento'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // File picker
              Card(
                child: InkWell(
                  onTap: _isUploading ? null : _pickFile,
                  borderRadius: BorderRadius.circular(16),
                  child: Padding(
                    padding: const EdgeInsets.all(32),
                    child: Column(
                      children: [
                        Icon(
                          _selectedFile == null
                              ? Icons.cloud_upload_outlined
                              : Icons.check_circle_outline,
                          size: 64,
                          color: _selectedFile == null
                              ? AppColors.primary
                              : AppColors.success,
                        ),
                        const SizedBox(height: 16),
                        Text(
                          _selectedFile == null
                              ? 'Seleccionar Archivo'
                              : _selectedFile!.path.split('/').last,
                          style: Theme.of(context).textTheme.titleMedium,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'PDF, Word, o Imagen',
                          style:
                              Theme.of(context).textTheme.bodySmall?.copyWith(
                                    color: AppColors.textSecondary,
                                  ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),

              const SizedBox(height: 24),

              // Document type
              DropdownButtonFormField<String>(
                value: _documentType,
                decoration: const InputDecoration(
                  labelText: 'Tipo de Documento',
                  prefixIcon: Icon(Icons.category),
                ),
                items: _documentTypes.map((type) {
                  return DropdownMenuItem(
                    value: type['value'],
                    child: Text(type['label']!),
                  );
                }).toList(),
                onChanged: _isUploading
                    ? null
                    : (value) {
                        setState(() => _documentType = value!);
                      },
              ),

              const SizedBox(height: 16),

              // Name
              TextFormField(
                controller: _nameController,
                decoration: const InputDecoration(
                  labelText: 'Nombre del Documento',
                  prefixIcon: Icon(Icons.title),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Ingresa un nombre';
                  }
                  return null;
                },
                enabled: !_isUploading,
              ),

              const SizedBox(height: 16),

              // Description
              TextFormField(
                controller: _descriptionController,
                decoration: const InputDecoration(
                  labelText: 'Descripción (opcional)',
                  prefixIcon: Icon(Icons.description),
                ),
                maxLines: 3,
                enabled: !_isUploading,
              ),

              const SizedBox(height: 32),

              // Upload button
              ElevatedButton.icon(
                onPressed:
                    (_isUploading || _isProcessing || _selectedFile == null)
                        ? null
                        : _uploadDocument,
                icon: _isUploading || _isProcessing
                    ? const SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Icon(Icons.upload),
                label: Text(
                  _isUploading
                      ? 'Subiendo...'
                      : _isProcessing
                          ? 'Procesando...'
                          : 'Subir Documento',
                ),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                ),
              ),

              if (_isProcessing) ...[
                const SizedBox(height: 16),
                const LinearProgressIndicator(),
                const SizedBox(height: 8),
                Text(
                  'Procesando con IA...',
                  textAlign: TextAlign.center,
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                        color: AppColors.textSecondary,
                      ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
