"""
Script to verify the accuracy of the trained model
"""
import joblib
from pathlib import Path

def verify_model():
    model_path = Path('data/modelo_seguridad_final.pkl')
    
    if not model_path.exists():
        print(f"❌ Model not found at: {model_path}")
        return
    
    print("Loading model...")
    model_data = joblib.load(model_path)
    
    print("\n" + "="*60)
    print("MODEL VERIFICATION REPORT")
    print("="*60)
    
    # Check model structure
    if isinstance(model_data, dict):
        print("\n📦 Model Components:")
        for key in model_data.keys():
            print(f"  - {key}")
        
        # Extract accuracy if available
        if 'test_accuracy' in model_data:
            accuracy = model_data['test_accuracy']
            print(f"\n✅ Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
            
            if accuracy >= 0.82:
                print(f"   ✅ PASSED: Model meets 82% accuracy requirement!")
            else:
                print(f"   ❌ FAILED: Model accuracy ({accuracy*100:.2f}%) is below 82% threshold")
        
        # Show other metrics
        if 'metrics' in model_data:
            print("\n📊 Additional Metrics:")
            for metric, value in model_data['metrics'].items():
                print(f"  - {metric}: {value:.4f}")
        
        # Show hyperparameters
        if 'best_params' in model_data:
            print("\n⚙️  Best Hyperparameters:")
            for param, value in model_data['best_params'].items():
                print(f"  - {param}: {value}")
        
        # Show cross-validation score
        if 'cv_score' in model_data:
            cv_score = model_data['cv_score']
            print(f"\n🔄 Cross-Validation Score: {cv_score:.4f} ({cv_score*100:.2f}%)")
    else:
        print("\n⚠️  Model is a raw classifier without metrics")
        print("   Type:", type(model_data))
    
    print("\n" + "="*60)
    print(f"Model file size: {model_path.stat().st_size / (1024*1024):.2f} MB")
    print("="*60)

if __name__ == "__main__":
    verify_model()
