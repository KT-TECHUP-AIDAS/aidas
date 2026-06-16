# storage.tf
# 이미지 저장용 S3 버킷
resource "aws_s3_bucket" "images" {
  bucket = var.s3_image_bucket
  tags   = { Name = var.s3_image_bucket }
}

# 퍼블릭 접근 허용 (이미지 공개)
resource "aws_s3_bucket_public_access_block" "images" {
  bucket                  = aws_s3_bucket.images.id
  block_public_acls       = false ## 퍼블릭 허용
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# 버킷 정책 - 퍼블릭 읽기 허용
resource "aws_s3_bucket_policy" "images" {
  bucket     = aws_s3_bucket.images.id
  depends_on = [aws_s3_bucket_public_access_block.images]

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "PublicReadGetObject"
      Effect    = "Allow"
      Principal = "*"            # ← 누구나
      Action    = "s3:GetObject" # ← 읽기만
      Resource  = "${aws_s3_bucket.images.arn}/*"
    }]
  })
}

# CORS 설정 (dafarm.shop에서 s3.amazonaws.com 이미지를 접근허용)
resource "aws_s3_bucket_cors_configuration" "images" {
  bucket = aws_s3_bucket.images.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET"]
    allowed_origins = [
    "https://www.${var.domain_name}",
    "https://${var.domain_name}",
    "https://${aws_cloudfront_distribution.main.domain_name}"
    ]
    expose_headers  = ["ETag"]
    max_age_seconds = 3600
  }
}