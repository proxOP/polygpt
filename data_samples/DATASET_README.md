# Verification Dataset Samples

Collected additional dataset samples for the verification journey.

- Recaptured images from multiple phones (Android, iPhone) to increase device diversity.
- Each capture set includes: front ID, back ID, selfie, and environment/context photos.
- Samples are grouped by `capture_session_{timestamp}` and device model when available.

Notes:
- Images are stored separately outside the repository due to size and privacy.
- Metadata schema example: `session_id`, `device_model`, `capture_time`, `image_type`, `quality_score`.

Purpose:
- These samples are used for testing the verification pipeline, liveness checks, and model robustness across capture devices.
