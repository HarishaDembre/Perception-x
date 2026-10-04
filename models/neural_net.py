"""
PyTorch Hierarchical Neural Network for Perception-X
Solves the exact dual-stage task:
1. Gating Head: Is the image an Object or an Illusion?
2. Illusion Head: If it is an illusion, which kind of illusion is it?
   - Geometric & Distortion
   - Brightness & Contrast
   - Ambiguous & Multistable
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

class PerceptionXHierarchicalNet(nn.Module):
    def __init__(self, num_illusion_classes=3):
        super(PerceptionXHierarchicalNet, self).__init__()
        
        # Convolutional Feature Extractor
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        
        self.conv4 = nn.Conv2d(128, 128, kernel_size=3, padding=1)
        self.bn4 = nn.BatchNorm2d(128)
        
        self.pool = nn.MaxPool2d(2, 2)
        self.gap = nn.AdaptiveAvgPool2d((4, 4))
        
        # Shared Embedding Space
        self.fc_shared = nn.Linear(128 * 4 * 4, 256)
        self.dropout = nn.Dropout(0.3)
        
        # Head 1: Object vs Illusion (2 classes: 0 = Object, 1 = Illusion)
        self.head_gating = nn.Linear(256, 2)
        
        # Head 2: Which Kind of Illusion (3 classes: Geometric, Brightness, Ambiguous)
        self.head_illusion = nn.Linear(256, num_illusion_classes)

    def forward(self, x):
        # Feature extraction
        x = self.pool(F.relu(self.bn1(self.conv1(x)))) # 128 -> 64
        x = self.pool(F.relu(self.bn2(self.conv2(x)))) # 64 -> 32
        x = self.pool(F.relu(self.bn3(self.conv3(x)))) # 32 -> 16
        x = F.relu(self.bn4(self.conv4(x)))            # 16 -> 16
        x = self.gap(x)                                # 16 -> 4x4
        
        feat = x.view(x.size(0), -1)
        feat = self.dropout(F.relu(self.fc_shared(feat)))
        
        # Dual-Head Outputs
        gating_logits = self.head_gating(feat)
        illusion_logits = self.head_illusion(feat)
        
        return gating_logits, illusion_logits
